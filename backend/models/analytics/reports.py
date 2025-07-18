"""
Analytics report models.

This module contains models for report generation and analytics data structures.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ReportMetadata(BaseModel):
    """Metadata for analytics reports."""
    
    report_id: str = Field(..., description="Unique report identifier")
    report_type: str = Field(..., description="Type of report")
    generated_at: datetime = Field(..., description="Report generation timestamp")
    time_range: Optional[str] = Field(None, description="Time range for report data")
    filters: Optional[Dict[str, Any]] = Field(None, description="Applied filters")


class SourceAnalytics(BaseModel):
    """Analytics data for content sources."""
    
    source: str = Field(..., description="Content source name")
    article_count: int = Field(..., description="Number of articles from this source")
    avg_engagement: Optional[float] = Field(None, description="Average engagement score")
    top_tags: List[str] = Field(default_factory=list, description="Most common tags")


class CategoryAnalytics(BaseModel):
    """Analytics data for article categories."""
    
    category: str = Field(..., description="Article category")
    article_count: int = Field(..., description="Number of articles in this category")
    engagement_rate: Optional[float] = Field(None, description="Engagement rate for category")
    trending: bool = Field(False, description="Whether category is trending")


class UserEngagementReport(BaseModel):
    """Report for user engagement analytics."""
    
    metadata: ReportMetadata
    total_users: int = Field(..., description="Total number of users")
    active_users: int = Field(..., description="Number of active users")
    avg_session_duration: Optional[float] = Field(None, description="Average session duration")
    top_interactions: List[Dict[str, Any]] = Field(default_factory=list, description="Top user interactions")


class ContentPerformanceReport(BaseModel):
    """Report for content performance analytics."""
    
    metadata: ReportMetadata
    total_articles: int = Field(..., description="Total number of articles")
    sources: List[SourceAnalytics] = Field(default_factory=list, description="Analytics by source")
    categories: List[CategoryAnalytics] = Field(default_factory=list, description="Analytics by category")
    top_performing: List[Dict[str, Any]] = Field(default_factory=list, description="Top performing articles") 