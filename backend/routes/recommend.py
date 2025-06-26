from fastapi import APIRouter, Query
from engine.recommender import recommend_articles
from logging_config import logger

router = APIRouter()

@router.get("/recommend")
def get_recommendations(
    query: str = Query(""),
    top_k: int = Query(5),
    user_id: str = Query(None)
):
    logger.info(f"📥 Incoming recommendation request | query='{query}', user_id={user_id}")
    
    try:
        results = recommend_articles(query, top_k=top_k, user_id=user_id)
        logger.info(f"✅ Returning {len(results)} recommendations")
        return {"results": results}
    except Exception as e:
        logger.exception("❌ Error generating recommendations")
        return {"error": str(e)}
