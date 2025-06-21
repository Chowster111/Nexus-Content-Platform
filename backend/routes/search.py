# routes/search.py
from fastapi import APIRouter, Query
from sentence_transformers import util
from db.supabase_client import supabase
from .utils.embedding_utils import safe_encode, semantic_model
import numpy as np

router = APIRouter()

@router.get("/articles")
def search_articles(q: str = Query(..., description="Search query")):
    query_embedding = safe_encode(q, semantic_model)
    if query_embedding is None:
        return {"error": "Failed to embed query"}

    try:
        response = (
            supabase
            .table("articles")
            .select("*")
            .order("published_date", desc=True)
            .execute()
        )
    except Exception as e:
        print("Error: {e}")
        return {"error": str(e)}
    
    articles = response.data
    if not articles:
        return {"results": []}

    scores = []
    for article in articles:
        emb = article.get("embedding")
        if emb:
            similarity = util.cos_sim(query_embedding, [emb])[0][0].item()
            scores.append((similarity, article))

    sorted_results = sorted(scores, key=lambda x: x[0], reverse=True)
    top_results = [
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
        for source, article in sorted_results[:10]
    ]

    return {"results": top_results}
