"""
Likes models for user article interactions.

This module contains Pydantic models for handling user likes/dislikes
of articles, including request/response structures and validation.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class LikeRequest(BaseModel):
    """Request model for individual article like/dislike."""
    
    article_id: str = Field(..., description="Unique identifier for the article")
    user_id: str = Field(..., description="User identifier")
    url: Optional[str] = Field(None, description="Article URL")
    liked: bool = Field(..., description="Whether the user liked (True) or disliked (False) the article")
    
    @validator('article_id')
    def validate_article_id(cls, v):
        if not v or not v.strip():
            raise ValueError("article_id cannot be empty")
        return v.strip()
    
    @validator('user_id')
    def validate_user_id(cls, v):
        if not v or not v.strip():
            raise ValueError("user_id cannot be empty")
        return v.strip()


class LikeResponse(BaseModel):
    """Response model for like operations."""
    
    message: str = Field(..., description="Success/error message")
    liked: bool = Field(..., description="Whether the operation was successful")
    count: Optional[int] = Field(None, description="Number of likes processed")
    errors: Optional[List[Dict[str, Any]]] = Field(None, description="Any validation errors encountered")


class LikeRecord(BaseModel):
    """Database record model for likes table."""
    
    id: Optional[int] = Field(None, description="Primary key")
    user_id: str = Field(..., description="User identifier")
    article_url: str = Field(..., description="Article URL")
    liked: bool = Field(..., description="Like/dislike status")
    created_at: Optional[datetime] = Field(None, description="Timestamp of like creation")
    
    class Config:
        from_attributes = True 