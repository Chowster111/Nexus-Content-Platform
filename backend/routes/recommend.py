from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query, HTTPException
from engine.recommender import recommend_articles
from logging_config import logger
from .utils.retry import with_backoff
from ..models.models import RecommendationRequest, RecommendationResponse, ArticleResponse


class RecommendController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self) -> None:
        """Register all recommendation routes."""
        @self.router.get("/recommend", response_model=RecommendationResponse)
        def get_recommendations(
            query: str = Query("", description="Query for recommendations"),
            top_k: int = Query(5, ge=1, le=50, description="Number of top results"),
            user_id: Optional[str] = Query(None, description="Optional user ID for personalization")
        ) -> RecommendationResponse:
            """Get article recommendations based on query and user preferences."""
            logger.info(f"Incoming recommendation request | query='{query}', user_id={user_id}")

            try:
                results: List[Dict[str, Any]] = self.get_recommendation_results(query, top_k, user_id)
                logger.info(f"SUCCESS Returning {len(results)} recommendations")
                return RecommendationResponse(articles=[ArticleResponse(**article) for article in results])
            except Exception as e:
                logger.exception("ERROR generating recommendations after retries")
                return RecommendationResponse(error=str(e))

    @with_backoff()
    def get_recommendation_results(self, query: str, top_k: int, user_id: Optional[str]) -> List[Dict[str, Any]]:
        """Get recommendation results from the recommender engine."""
        return recommend_articles(query, top_k=top_k, user_id=user_id)
