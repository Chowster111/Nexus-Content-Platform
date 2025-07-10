from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Request, HTTPException
from db.supabase_client import supabase
from logging_config import logger
from .utils.retry import with_backoff
from models.likes import LikeRequest, LikeResponse
from pydantic import ValidationError


class LikesController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self) -> None:
        """Register all likes routes."""
        @self.router.post("/likes", response_model=LikeResponse)
        async def save_likes(request: Request) -> LikeResponse:
            """Save user likes for articles."""
            try:
                body: Dict[str, Any] = await request.json()
                user_id: Optional[str] = body.get("user_id")
                likes: List[Dict[str, Any]] = body.get("likes", [])

                if not user_id or not isinstance(likes, list):
                    logger.warning(f"INVALID payload received: {body}")
                    raise HTTPException(status_code=400, detail="Missing user_id or likes list")

                insert_payload: List[Dict[str, Any]] = []
                errors = []
                for article in likes:
                    try:
                        # Validate LikeRequest structure
                        LikeRequest(article_id=article.get("article_id", ""), user_id=user_id)
                        insert_payload.append({
                        "user_id": user_id,
                        "article_url": article.get("url", ""),
                        "liked": article.get("liked", False),
                        })
                    except ValidationError as ve:
                        logger.error(f"Validation error for like: {article} | {ve}")
                        errors.append({"like": article, "error": str(ve)})
                if errors:
                    logger.warning(f"Some likes could not be validated: {errors}")

                if insert_payload:
                    self.insert_likes(insert_payload)

                logger.info(f"SAVED {len(insert_payload)} likes for user {user_id}")
                return LikeResponse(message=f"{len(insert_payload)} likes saved", liked=True)

            except Exception as e:
                logger.exception("ERROR: Failed to save likes")
                raise HTTPException(status_code=500, detail="Internal server error")

    @with_backoff()
    def insert_likes(self, payload: List[Dict[str, Any]]) -> None:
        """Insert likes into the database."""
        logger.info(f"SUCCESS Inserting {len(payload)} likes into Supabase")
        supabase.table("likes").insert(payload).execute()
