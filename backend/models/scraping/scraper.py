from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class ScraperConfig(BaseModel):
    """
    Configuration model for web scrapers.
    """
    source_name: str
    base_url: str
    scroll_limit: int = Field(default=30, ge=0)
    max_pages: Optional[int] = None

class ScrapedArticle(BaseModel):
    """
    Model for articles during scraping process.
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
    """
    articles: List[ScrapedArticle] = Field(default_factory=list)
    source: str
    success: bool
    error: Optional[str] = None 