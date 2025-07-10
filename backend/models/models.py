# This file now re-exports models from submodules for backward compatibility.
# Please import models directly from their respective files for new code.

from .article import Article, ArticleResponse, ArticleCategory, ArticleSource
from .user import User
from .auth import SignupRequest, SigninRequest, AuthResponse
from .analytics import TagCount
from .recommendation import RecommendationRequest, RecommendationResponse
from .scraper import ScraperConfig, ScrapedArticle, ScraperResult
from .likes import LikeRequest, LikeResponse, LikeRecord
from .search import SearchResult, SearchResponse, SearchRequest
from .health import HealthCheckResponse, SystemStatus, DetailedHealthResponse

# If any models remain here, move them to the appropriate submodule.