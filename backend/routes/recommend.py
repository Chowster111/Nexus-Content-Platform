from fastapi import APIRouter, Query
from engine.recommender import recommend_articles

router = APIRouter()

@router.get("/recommend")
def get_recommendations(query: str = Query(...), top_k: int = Query(5)):
    try:
        print(f"📥 Incoming query: {query}")
        results = recommend_articles(query, top_k)
        print(f"✅ Found {len(results)} recommendations")
        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}
