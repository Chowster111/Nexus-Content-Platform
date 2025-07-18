from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

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
    """
    title: str
    url: str
    published_date: Optional[datetime] = None
    source: str
    tags: List[str] = Field(default_factory=list)
    category: str
    summary: Optional[str] = None 