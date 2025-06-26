from fastapi import APIRouter, Request, HTTPException
from db.supabase_client import supabase
from logging_config import logger

router = APIRouter()

@router.post("/likes")
async def save_likes(request: Request):
    try:
        body = await request.json()
        user_id = body.get("user_id")
        likes = body.get("likes", [])

        if not user_id or not isinstance(likes, list):
            logger.warning(f"Invalid payload received: {body}")
            raise HTTPException(status_code=400, detail="Missing user_id or likes list")

        insert_payload = []
        for article in likes:
            insert_payload.append({
                "user_id": user_id,
                "article_url": article.get("url", ""),
                "liked": article.get("liked", False),
            })

        if insert_payload:
            supabase.table("likes").insert(insert_payload).execute()

        logger.info(f"Saved {len(insert_payload)} likes for user {user_id}")
        return {"message": f"{len(insert_payload)} likes saved"}

    except Exception as e:
        logger.error(f"Failed to save likes: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
