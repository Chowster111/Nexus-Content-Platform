from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum
from .article import ArticleResponse


class SortOrder(str, Enum):
    """Sort order enumeration for article queries."""
    LATEST = "latest"
    OLDEST = "oldest"

class RecommendationRequest(BaseModel):
    """
    Recommendation request model.
    """
    user_id: str = Field(..., description="User ID for recommendations")
    limit: Optional[int] = Field(default=10, ge=1, le=50, description="Number of recommendations")

class RecommendationResponse(BaseModel):
    """
    Recommendation response wrapper with error handling.
    """
    articles: List[ArticleResponse] = Field(default_factory=list)
    error: Optional[str] = None 