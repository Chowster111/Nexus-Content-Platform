from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query, HTTPException
from engine.recommender import recommend_articles
from logging_config import logger
from .utils.retry import with_backoff
from models.recommendation import RecommendationRequest, RecommendationResponse
from models.article import ArticleResponse
from pydantic import ValidationError


class RecommendController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self) -> None:
        """Register all recommendation routes."""
        @self.router.get(
            "/recommend", 
            response_model=RecommendationResponse,
            summary="Get Article Recommendations",
            description="""
            Get personalized article recommendations based on query and user preferences.
            
            This endpoint provides AI-powered article recommendations using a combination of:
            - Semantic similarity with BGE embeddings
            - User preference learning from likes/dislikes
            - Content-based filtering by category and tags
            - Collaborative filtering based on similar user behavior
            
            **Recommendation Algorithm:**
            1. **Query Processing**: Converts natural language query to embeddings
            2. **Content Matching**: Finds articles with similar semantic content
            3. **User Personalization**: Incorporates user's like/dislike history
            4. **Diversity Boost**: Ensures variety in recommended articles
            5. **Freshness Weight**: Prioritizes recent articles when relevant
            
            **Personalization Features:**
            - Learns from user's like/dislike interactions
            - Considers user's preferred categories and sources
            - Adapts recommendations based on reading patterns
            - Provides both similar and diverse article suggestions
            
            **Response Quality:**
            - Articles are ranked by relevance score (0-1)
            - Each article includes similarity score and reasoning
            - Handles cold-start scenarios for new users
            - Gracefully degrades when user data is unavailable
            """,
            response_description="List of recommended articles with relevance scores and metadata",
            tags=["Recommendations"]
        )
        def get_recommendations(
            query: str = Query(
                "", 
                description="Natural language query for recommendations",
                example="machine learning deployment strategies",
                max_length=500
            ),
            top_k: int = Query(
                5, 
                ge=1, 
                le=50, 
                description="Number of recommendations to return (1-50)"
            ),
            user_id: Optional[str] = Query(
                None, 
                description="User ID for personalized recommendations"
            )
        ) -> RecommendationResponse:
            """
            Get personalized article recommendations.
            
            Returns a curated list of articles that match the user's interests and the provided query.
            The recommendations are personalized based on the user's interaction history and preferences.
            
            **Parameters:**
            - `query`: Natural language description of what you're looking for
            - `top_k`: Number of recommendations (1-50, default: 5)
            - `user_id`: Optional user ID for personalization
            
            **Example Usage:**
            ```
            GET /find/recommend?query=scalable architecture&top_k=10&user_id=user123
            ```
            
            **Response Example:**
            ```json
            {
              "articles": [
                {
                  "title": "Building Scalable Microservices",
                  "url": "https://netflix.com/tech-blog/scalable-microservices",
                  "published_date": "2024-01-15",
                  "source": "netflix",
                  "category": "Architecture",
                  "tags": ["microservices", "scalability", "architecture"],
                  "summary": "How Netflix built their scalable microservices architecture...",
                  "similarity_score": 0.92
                }
              ],
              "error": null
            }
            ```
            
            **Error Scenarios:**
            - Returns empty list if no recommendations found
            - Handles embedding failures gracefully
            - Logs validation errors for debugging
            - Provides fallback recommendations for new users
            """
            logger.info(f"Incoming recommendation request | query='{query}', user_id={user_id}")

            try:
                results: List[Dict[str, Any]] = self.get_recommendation_results(query, top_k, user_id)
                logger.info(f"SUCCESS Returning {len(results)} recommendations")
                articles = []
                errors = []
                for article in results:
                    try:
                        articles.append(ArticleResponse(**article))
                    except ValidationError as ve:
                        logger.error(f"Validation error for article: {article} | {ve}")
                        errors.append({"article": article, "error": str(ve)})
                if errors:
                    logger.warning(f"Some articles could not be validated: {errors}")
                return RecommendationResponse(articles=articles, error=(f"{len(errors)} articles failed validation" if errors else None))
            except Exception as e:
                logger.exception("ERROR generating recommendations after retries")
                return RecommendationResponse(error=f"Internal error: {e}")

    @with_backoff()
    def get_recommendation_results(self, query: str, top_k: int, user_id: Optional[str]) -> List[Dict[str, Any]]:
        """Get recommendation results from the recommender engine."""
        return recommend_articles(query, top_k=top_k, user_id=user_id)
