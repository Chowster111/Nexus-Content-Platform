from fastapi import APIRouter, Query, HTTPException
from engine.recommender import recommend_articles
from logging_config import logger
from .utils.retry import with_backoff

class RecommendController:
    def __init__(self):
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self):
        @self.router.get("/recommend")
        def get_recommendations(
            query: str = Query("", description="Query for recommendations"),
            top_k: int = Query(5, description="Number of top results"),
            user_id: str = Query(None, description="Optional user ID for personalization")
        ):
            logger.info(f"📥 Incoming recommendation request | query='{query}', user_id={user_id}")

            try:
                results = self.get_recommendation_results(query, top_k, user_id)
                logger.info(f"✅ Returning {len(results)} recommendations")
                return results
            except Exception as e:
                logger.exception("❌ Error generating recommendations after retries")
                raise HTTPException(status_code=500, detail=str(e))

    @with_backoff()
    def get_recommendation_results(self, query: str, top_k: int, user_id: str):
        return recommend_articles(query, top_k=top_k, user_id=user_id)
