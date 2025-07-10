from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class SortOrder(str, Enum):
    LATEST = "latest"
    OLDEST = "oldest"


class ArticleCategory(str, Enum):
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
    title: str
    url: str
    published_date: Optional[datetime] = None
    source: str
    tags: List[str] = Field(default_factory=list)
    category: str
    summary: Optional[str] = None


class TagCount(BaseModel):
    tag: str
    count: int


class SearchResult(BaseModel):
    title: str
    url: str
    published_date: Optional[datetime] = None
    content: str = ""
    source: str = ""
    tags: List[str] = Field(default_factory=list)
    category: str = ""
    summary: str = ""


class SearchResponse(BaseModel):
    results: List[SearchResult] = Field(default_factory=list)
    error: Optional[str] = None


class User(BaseModel):
    id: str
    username: str
    email: str


class SignupRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")


class SigninRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class AuthResponse(BaseModel):
    message: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    user: Optional[Dict[str, Any]] = None


class LikeRequest(BaseModel):
    article_id: str = Field(..., description="Article ID to like/unlike")
    user_id: str = Field(..., description="User ID")


class LikeResponse(BaseModel):
    message: str
    liked: bool


class RecommendationRequest(BaseModel):
    user_id: str = Field(..., description="User ID for recommendations")
    limit: Optional[int] = Field(default=10, ge=1, le=50, description="Number of recommendations")


class RecommendationResponse(BaseModel):
    articles: List[ArticleResponse] = Field(default_factory=list)
    error: Optional[str] = None


class ScraperConfig(BaseModel):
    source_name: str
    base_url: str
    scroll_limit: int = Field(default=30, ge=0)
    max_pages: Optional[int] = None


class ScrapedArticle(BaseModel):
    title: str
    url: str
    published_date: Optional[datetime] = None
    source: str
    tags: List[str] = Field(default_factory=list)
    category: str
    embedding: Optional[List[float]] = None
    summary: Optional[str] = None


class ScraperResult(BaseModel):
    articles: List[ScrapedArticle] = Field(default_factory=list)
    source: str
    success: bool
    error: Optional[str] = None