from fastapi import APIRouter, Query
from sentence_transformers import util
from db.supabase_client import supabase
from .utils.embedding_utils import safe_encode, semantic_model
from logging_config import logger
from .utils.retry import with_backoff

router = APIRouter()

@with_backoff()
def fetch_ranked_articles(query_embedding):
    response = (
        supabase
        .table("articles")
        .select("*")
        .order("published_date", desc=True)
        .execute()
    )
    logger.info("✅ Retrieved articles from Supabase")

    articles = response.data or []
    scores = []
    for article in articles:
        emb = article.get("embedding")
        if emb:
            similarity = util.cos_sim(query_embedding, [emb])[0][0].item()
            scores.append((similarity, article))

    sorted_results = sorted(scores, key=lambda x: x[0], reverse=True)
    return [
        {
            "title": article["title"],
            "url": article["url"],
            "published_date": article["published_date"],
            "content": article.get("content", ""),
            "source": article.get("source", ""),
            "tags": article.get("tags", []),
            "category": article.get("category", ""),
            "summary": article.get("summary", ""),
        }
        for _, article in sorted_results[:10]
    ]


@router.get("/articles")
def search_articles(q: str = Query(..., description="Search query")):
    logger.info(f"🔍 Incoming search query: '{q}'")

    query_embedding = safe_encode(q, semantic_model)
    if query_embedding is None:
        logger.warning("⚠️ Failed to embed query")
        return {"error": "Failed to embed query"}

    try:
        top_results = fetch_ranked_articles(query_embedding)
        if not top_results:
            logger.info("📭 No articles found or matched")
            return {"results": []}

        logger.info(f"🎯 Returning top {len(top_results)} results")
        return {"results": top_results}
    except Exception as e:
        logger.exception("❌ Search failed after retries")
        return {"error": str(e)}
