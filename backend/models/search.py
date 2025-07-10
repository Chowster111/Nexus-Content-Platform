"""
Search models for article search functionality.

This module contains Pydantic models for search results and responses,
including validation for search result structures and error handling.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class SearchResult(BaseModel):
    """Individual search result model."""
    
    title: str = Field(..., description="Article title")
    url: str = Field(..., description="Article URL")
    published_date: datetime = Field(..., description="Publication date")
    content: str = Field(default="", description="Article content or excerpt")
    source: str = Field(default="", description="Source website or platform")
    tags: List[str] = Field(default_factory=list, description="Article tags")
    category: str = Field(default="", description="Article category")
    summary: str = Field(default="", description="Article summary")
    similarity_score: Optional[float] = Field(None, description="Similarity score from search")
    
    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("title cannot be empty")
        return v.strip()
    
    @validator('url')
    def validate_url(cls, v):
        if not v or not v.strip():
            raise ValueError("url cannot be empty")
        if not v.startswith(('http://', 'https://')):
            raise ValueError("url must be a valid HTTP/HTTPS URL")
        return v.strip()
    
    @validator('tags')
    def validate_tags(cls, v):
        if v is None:
            return []
        return [tag.strip() for tag in v if tag and tag.strip()]


class SearchResponse(BaseModel):
    """Response model for search operations."""
    
    results: List[SearchResult] = Field(default_factory=list, description="Search results")
    error: Optional[str] = Field(None, description="Error message if search failed")
    query: Optional[str] = Field(None, description="Original search query")
    total_count: Optional[int] = Field(None, description="Total number of results found")
    processing_time: Optional[float] = Field(None, description="Search processing time in seconds")
    
    @validator('results')
    def validate_results(cls, v):
        if v is None:
            return []
        return v
    
    @validator('error')
    def validate_error(cls, v):
        if v is not None and not v.strip():
            return None
        return v


class SearchRequest(BaseModel):
    """Request model for search operations."""
    
    query: str = Field(..., description="Search query string")
    limit: Optional[int] = Field(10, ge=1, le=100, description="Maximum number of results")
    offset: Optional[int] = Field(0, ge=0, description="Result offset for pagination")
    filters: Optional[Dict[str, Any]] = Field(None, description="Search filters")
    
    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError("query cannot be empty")
        return v.strip() 