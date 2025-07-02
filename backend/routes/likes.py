from fastapi import APIRouter, Request, HTTPException
from db.supabase_client import supabase
from logging_config import logger
from .utils.retry import with_backoff

class LikesController:
    def __init__(self):
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self):
        @self.router.post("/likes")
        async def save_likes(request: Request):
            try:
                body = await request.json()
                user_id = body.get("user_id")
                likes = body.get("likes", [])

                if not user_id or not isinstance(likes, list):
                    logger.warning(f"⚠️ Invalid payload received: {body}")
                    raise HTTPException(status_code=400, detail="Missing user_id or likes list")

                insert_payload = [
                    {
                        "user_id": user_id,
                        "article_url": article.get("url", ""),
                        "liked": article.get("liked", False),
                    }
                    for article in likes
                ]

                if insert_payload:
                    self.insert_likes(insert_payload)

                logger.info(f"👍 Saved {len(insert_payload)} likes for user {user_id}")
                return {"message": f"{len(insert_payload)} likes saved"}

            except Exception as e:
                logger.exception("❌ Failed to save likes")
                raise HTTPException(status_code=500, detail="Internal server error")

    @with_backoff()
    def insert_likes(self, payload):
        logger.info(f"📥 Inserting {len(payload)} likes into Supabase")
        supabase.table("likes").insert(payload).execute()
