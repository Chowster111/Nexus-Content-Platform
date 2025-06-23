from fastapi import APIRouter, Query
from engine.recommender import recommend_articles

router = APIRouter()

@router.get("/recommend")
def get_recommendations(
    query: str = Query(""),
    top_k: int = Query(5),
    user_id: str = Query(None)
):
    try:
        print(f"📥 Incoming query: {query}, user_id: {user_id}")
        results = recommend_articles(query, top_k=top_k, user_id=user_id)
        print(f"✅ Found {len(results)} recommendations")
        return {"results": results}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}
