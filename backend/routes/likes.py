from fastapi import APIRouter, Query, HTTPException, Request
from db.supabase_client import supabase

router = APIRouter()

@router.post("/likes")
async def save_likes(request: Request):
    try:
        body = await request.json()
    except Exception as e:
        print(f"Error: {e}")
        raise e
    user_id = body["user_id"]
    likes = body["likes"]

    for article in likes:
        supabase.table("likes").insert({
            "user_id": user_id,
            "article_url": article.get("url", ""),
            "liked": article["liked"],
        }).execute()

    return {"message": "Likes saved"}