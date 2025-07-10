# backend/routes/search_controller.py

from typing import List, Dict, Any, Tuple, Optional
from fastapi import APIRouter, Query
from sentence_transformers import util
from db.supabase_client import supabase
from .utils.embedding_utils import safe_encode, semantic_model
from logging_config import logger
from .utils.retry import with_backoff
from .models.search import SearchResult, SearchResponse
from pydantic import ValidationError


class SearchController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.add_api_route("/articles", self.search_articles, methods=["GET"])

    @with_backoff()
    def fetch_ranked_articles(self, query_embedding: List[float]) -> List[SearchResult]:
        """Fetch and rank articles based on query embedding."""
        response: Dict[str, Any] = (
            supabase
            .table("articles")
            .select("*")
            .order("published_date", desc=True)
            .execute()
        )
        logger.info("SUCCESS Retrieved articles from Supabase")

        articles: List[Dict[str, Any]] = response.data or []
        scores: List[Tuple[float, Dict[str, Any]]] = []
        
        for article in articles:
            emb: Optional[List[float]] = article.get("embedding")
            if emb:
                similarity: float = util.cos_sim(query_embedding, [emb])[0][0].item()
                scores.append((similarity, article))

        sorted_results: List[Tuple[float, Dict[str, Any]]] = sorted(scores, key=lambda x: x[0], reverse=True)
        
        top_results = []
        errors = []
        for _, article in sorted_results[:10]:
            try:
                top_results.append(SearchResult(
                title=article["title"],
                url=article["url"],
                published_date=article["published_date"],
                content=article.get("content", ""),
                source=article.get("source", ""),
                tags=article.get("tags", []),
                category=article.get("category", ""),
                summary=article.get("summary", ""),
                ))
            except ValidationError as ve:
                logger.error(f"Validation error for article: {article} | {ve}")
                errors.append({"article": article, "error": str(ve)})
        if errors:
            logger.warning(f"Some search results could not be validated: {errors}")
        return top_results

    async def search_articles(self, q: str = Query(..., description="Search query")) -> SearchResponse:
        """Search articles based on query."""
        logger.info(f"Incoming search query: '{q}'")

        query_embedding: Optional[List[float]] = safe_encode(q, semantic_model)
        if query_embedding is None:
            logger.warning("ERROR Failed to embed query")
            return SearchResponse(error="Failed to embed query")

        try:
            top_results: List[SearchResult] = self.fetch_ranked_articles(query_embedding)
            if not top_results:
                logger.info("No articles found or matched")
                return SearchResponse(results=[])

            logger.info(f"Returning top {len(top_results)} results")
            return SearchResponse(results=top_results)
        except Exception as e:
            logger.exception("ERROR: Search failed after retries")
            return SearchResponse(error=f"Internal error: {e}")
