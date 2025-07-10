from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from enum import Enum


class SortOrder(str, Enum):
    """Sort order for article queries."""
    LATEST = "latest"
    OLDEST = "oldest"


class ArticleCategory(str, Enum):
    """Categories for engineering articles."""
    ENGINEERING = "Engineering"
    PRODUCT = "Product"
    DATA_SCIENCE = "Data Science"
    SECURITY = "Security"
    INFRASTRUCTURE = "Infrastructure"
    MOBILE = "Mobile"
    WEB = "Web"
    MACHINE_LEARNING = "Machine Learning"
    DEVOPS = "DevOps"
    FRONTEND = "Frontend"
    BACKEND = "Backend"
    GENERAL = "General"


class ArticleSource(str, Enum):
    """Sources for engineering blog articles."""
    NETFLIX = "Netflix Tech Blog"
    AIRBNB = "Airbnb Engineering Blog"
    STRIPE = "Stripe Blog"
    TINDER = "Tinder Tech Blog"
    UBER = "Uber Engineering Blog"
    ROBINHOOD = "Robinhood Newsroom"
    META = "Meta Engineering Blog"
    DOORDASH = "DoorDash Engineering Blog"
    NOTION = "Notion Engineering Blog"
    SLACK = "Slack Engineering Blog"


class Article(BaseModel):
    """
    Core article model for internal processing.
    
    This model represents a complete article with all fields including embeddings.
    Used for database operations and internal data processing.
    
    Validation:
    - title: Required string
    - url: Required string (should be valid URL)
    - tags: List of strings (defaults to empty list)
    - embedding: Optional list of floats (768-dimensional vector)
    """
    id: Optional[str] = None
    title: str
    url: str
    published_date: Optional[datetime] = None
    source: str
    tags: List[str] = Field(default_factory=list)
    category: str
    embedding: Optional[List[float]] = None
    summary: Optional[str] = None
    content: Optional[str] = None


class ArticleResponse(BaseModel):
    """
    Article response model for API endpoints.
    
    This model is used for all article-related API responses.
    Excludes sensitive fields like embeddings and content.
    
    Validation:
    - All fields are validated at runtime
    - tags defaults to empty list if not provided
    - published_date is optional
    """
    title: str
    url: str
    published_date: Optional[datetime] = None
    source: str
    tags: List[str] = Field(default_factory=list)
    category: str
    summary: Optional[str] = None


class TagCount(BaseModel):
    """Model for tag statistics in analytics."""
    tag: str
    count: int


class SearchResult(BaseModel):
    """
    Search result model for semantic search responses.
    
    Includes content field for search result display.
    All fields have defaults to handle partial data gracefully.
    """
    title: str
    url: str
    published_date: Optional[datetime] = None
    content: str = ""
    source: str = ""
    tags: List[str] = Field(default_factory=list)
    category: str = ""
    summary: str = ""


class SearchResponse(BaseModel):
    """
    Search response wrapper with error handling.
    
    Can contain either search results or an error message.
    Used by all search-related endpoints.
    """
    results: List[SearchResult] = Field(default_factory=list)
    error: Optional[str] = None


class User(BaseModel):
    """User model for authentication responses."""
    id: str
    username: str
    email: str


class SignupRequest(BaseModel):
    """
    User signup request model.
    
    Validation:
    - email: Must be valid email format
    - password: Minimum 6 characters
    """
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")


class SigninRequest(BaseModel):
    """
    User signin request model.
    
    Validation:
    - email: Must be valid email format
    - password: Required field
    """
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class AuthResponse(BaseModel):
    """
    Authentication response model.
    
    Contains user data and tokens on successful auth.
    Can include error information on failed auth.
    """
    message: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    user: Optional[Dict[str, Any]] = None


class LikeRequest(BaseModel):
    """
    Article like/unlike request model.
    
    Validation:
    - article_id: Required string
    - user_id: Required string
    """
    article_id: str = Field(..., description="Article ID to like/unlike")
    user_id: str = Field(..., description="User ID")


class LikeResponse(BaseModel):
    """Response model for like operations."""
    message: str
    liked: bool


class RecommendationRequest(BaseModel):
    """
    Recommendation request model.
    
    Validation:
    - user_id: Required string
    - limit: Optional int between 1-50 (defaults to 10)
    """
    user_id: str = Field(..., description="User ID for recommendations")
    limit: Optional[int] = Field(default=10, ge=1, le=50, description="Number of recommendations")


class RecommendationResponse(BaseModel):
    """
    Recommendation response wrapper with error handling.
    
    Can contain either recommended articles or an error message.
    Used by all recommendation endpoints.
    """
    articles: List[ArticleResponse] = Field(default_factory=list)
    error: Optional[str] = None


class ScraperConfig(BaseModel):
    """
    Configuration model for web scrapers.
    
    Validation:
    - scroll_limit: Must be >= 0 (defaults to 30)
    - max_pages: Optional positive integer
    """
    source_name: str
    base_url: str
    scroll_limit: int = Field(default=30, ge=0)
    max_pages: Optional[int] = None


class ScrapedArticle(BaseModel):
    """
    Model for articles during scraping process.
    
    Similar to Article but used specifically for scraped data validation.
    Includes embedding field for processing scraped articles.
    """
    title: str
    url: str
    published_date: Optional[datetime] = None
    source: str
    tags: List[str] = Field(default_factory=list)
    category: str
    embedding: Optional[List[float]] = None
    summary: Optional[str] = None


class ScraperResult(BaseModel):
    """
    Scraper operation result model.
    
    Contains scraped articles and operation status.
    Used by all scraper endpoints.
    """
    articles: List[ScrapedArticle] = Field(default_factory=list)
    source: str
    success: bool
    error: Optional[str] = None