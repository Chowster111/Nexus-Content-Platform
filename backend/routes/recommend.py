from fastapi import APIRouter, Query
from engine.recommender import recommend_articles
from logging_config import logger
from .utils.retry import with_backoff

router = APIRouter()

@with_backoff()
def get_recommendation_results(query: str, top_k: int, user_id):
    return recommend_articles(query, top_k=top_k, user_id=user_id)

@router.get("/recommend")
def get_recommendations(
    query: str = Query(""),
    top_k: int = Query(5),
    user_id: str = Query(None)
):
    logger.info(f"📥 Incoming recommendation request | query='{query}', user_id={user_id}")

    try:
        results = get_recommendation_results(query, top_k, user_id)
        logger.info(f"✅ Returning {len(results)} recommendations")
        return results
    except Exception as e:
        logger.exception("❌ Error generating recommendations after retries")
        return {"error": str(e)}
