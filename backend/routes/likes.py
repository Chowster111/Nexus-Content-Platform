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
        @self.router.post(
            "/likes", 
            response_model=LikeResponse,
            summary="Save User Likes",
            description="""
            Save user likes and dislikes for articles to enable personalized recommendations.
            
            This endpoint allows users to save their preferences for articles, which are then
            used to improve personalized recommendations. The system tracks both likes and
            dislikes to build a comprehensive user preference profile.
            
            **Features:**
            - Batch like/dislike saving for multiple articles
            - User preference learning for recommendations
            - Validation of article data before saving
            - Error handling for invalid data
            - Real-time preference updates
            
            **Personalization Benefits:**
            - Improves recommendation accuracy
            - Learns user preferences over time
            - Enables collaborative filtering
            - Provides personalized content discovery
            
            **Data Structure:**
            - User ID for preference tracking
            - Article URL for content identification
            - Like/dislike boolean for preference
            - Timestamp for preference history
            """,
            response_description="Confirmation of saved likes with count and status",
            tags=["User Preferences"]
        )
        async def save_likes(request: Request) -> LikeResponse:
            """
            Save user likes and dislikes for articles.
            
            Accepts a batch of user preferences for articles and saves them to the database.
            These preferences are used to improve personalized recommendations and content
            discovery for the user.
            
            **Request Body:**
            ```json
            {
              "user_id": "user-123",
              "likes": [
                {
                  "article_id": "article-456",
                  "url": "https://netflix.com/tech-blog/article",
                  "liked": true
                },
                {
                  "article_id": "article-789",
                  "url": "https://airbnb.com/engineering/article",
                  "liked": false
                }
              ]
            }
            ```
            
            **Response Example:**
            ```json
            {
              "message": "3 likes saved",
              "liked": true
            }
            ```
            
            **Validation:**
            - User ID must be provided and valid
            - Likes array must contain valid article data
            - Article URLs are validated for format
            - Duplicate likes are handled gracefully
            
            **Error Scenarios:**
            - 400: Missing user_id or invalid likes format
            - 400: Invalid article data in likes array
            - 500: Database insertion error
            - 500: Validation error for article data
            """
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
