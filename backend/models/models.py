"""
Backward compatibility module for models.

This file re-exports models from the new organized structure to maintain
backward compatibility with existing code. For new code, import directly
from the specific submodules.
"""

# Core domain models
from .core import (
    Article, ArticleResponse, ArticleCategory, ArticleSource, User,
    BaseEntity, BaseResponse, PaginationParams, SortParams, FilterParams
)

# API request/response models
from .api import (
    SignupRequest, SigninRequest, AuthResponse,
    SearchRequest, SearchResponse, SearchResult,
    RecommendationRequest, RecommendationResponse, SortOrder,
    LikeRequest, LikeResponse, LikeRecord
)

# Analytics models
from .analytics import (
    TagCount, ReportMetadata, SourceAnalytics, CategoryAnalytics,
    UserEngagementReport, ContentPerformanceReport
)

# System models
from .system import (
    HealthCheckResponse, SystemStatus, DetailedHealthResponse,
    MetricPoint, SystemMetric, AlertRule, Alert,
    ServiceStatus, SystemOverview
)

# Scraping models
from .scraping import ScraperConfig, ScrapedArticle, ScraperResult

# For backward compatibility, export all models
__all__ = [
    # Core models
    "Article",
    "ArticleResponse",
    "ArticleCategory", 
    "ArticleSource",
    "User",
    "BaseEntity",
    "BaseResponse",
    "PaginationParams",
    "SortParams",
    "FilterParams",
    
    # API models
    "SignupRequest",
    "SigninRequest",
    "AuthResponse",
    "SearchRequest",
    "SearchResponse", 
    "SearchResult",
    "RecommendationRequest",
    "RecommendationResponse",
    "SortOrder",
    "LikeRequest",
    "LikeResponse",
    "LikeRecord",
    
    # Analytics models
    "TagCount",
    "ReportMetadata",
    "SourceAnalytics",
    "CategoryAnalytics",
    "UserEngagementReport",
    "ContentPerformanceReport",
    
    # System models
    "HealthCheckResponse",
    "SystemStatus",
    "DetailedHealthResponse",
    "MetricPoint",
    "SystemMetric",
    "AlertRule",
    "Alert",
    "ServiceStatus",
    "SystemOverview",
    
    # Scraping models
    "ScraperConfig",
    "ScrapedArticle", 
    "ScraperResult"
]