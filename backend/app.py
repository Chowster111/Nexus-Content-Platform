from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager
from logging_config import logger

from routes.analytics import AnalyticsController
from routes.articles import ArticlesController
from routes.auth import AuthController
from routes.likes import LikesController
from routes.recommend import RecommendController
from routes.scraper import ScraperController
from routes.health import HealthController
from routes.search import SearchController
from config import settings, get_environment, get_cors_origins, get_rate_limits

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 FastAPI application is starting up in {get_environment()} environment")
    yield
    logger.info("🛑 FastAPI application is shutting down")

app = FastAPI(
    title=settings.app_name,
    description="""
    ## 🚀 Engineering Blog Recommender API
    
    A modern, AI-powered API for discovering and recommending high-quality engineering articles from top tech companies.
    
    ### Key Features
    
    * **Semantic Search**: Find articles using natural language queries with BGE embeddings
    * **Personalized Recommendations**: Get tailored article suggestions based on user preferences
    * **Multi-Source Scraping**: Automated collection from Netflix, Airbnb, Uber, Stripe, and more
    * **User Authentication**: Secure user management with Supabase Auth
    * **Analytics & Insights**: Track article popularity, source performance, and user engagement
    * **Real-time Health Monitoring**: Comprehensive health checks and Prometheus metrics
    
    ### Authentication
    
    Most endpoints require authentication. Use the `/auth/signup` and `/auth/signin` endpoints to get your access token.
    
    ### Rate Limiting
    
    * Search: 100 requests/minute
    * Recommendations: 50 requests/minute
    * Scraping: 10 requests/minute (admin only)
    
    ### Error Handling
    
    All endpoints return consistent error responses with detailed messages and appropriate HTTP status codes.
    
    ### Data Models
    
    All request/response models are validated using Pydantic for type safety and automatic documentation.
    """,
    version=settings.app_version,
    contact={
        "name": "Engineering Blog Recommender Team",
        "url": "https://github.com/yourusername/engineering-blog-recommender",
        "email": "api@engineeringblogrecommender.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "Search",
            "description": "Semantic search operations for finding relevant articles using natural language queries.",
        },
        {
            "name": "Recommendations", 
            "description": "AI-powered article recommendations based on user preferences and content similarity.",
        },
        {
            "name": "Articles",
            "description": "Article management operations including filtering, categorization, and metadata retrieval.",
        },
        {
            "name": "Scraping",
            "description": "Content scraping operations for collecting articles from various engineering blogs.",
        },
        {
            "name": "Analytics",
            "description": "Usage analytics and insights about article popularity, source performance, and user engagement.",
        },
        {
            "name": "Authentication",
            "description": "User authentication and session management operations.",
        },
        {
            "name": "User Preferences",
            "description": "User-specific operations like likes, bookmarks, and personalization data.",
        },
        {
            "name": "Health",
            "description": "System health checks and monitoring endpoints for production observability.",
        },
    ],
    lifespan=lifespan,
)

# Configure CORS based on environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=settings.api.cors_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize controllers based on feature flags
controllers = []

if settings.features.enable_search:
    controllers.append(SearchController())

if settings.features.enable_recommendations:
    controllers.append(RecommendController())

if settings.features.enable_scraping:
    controllers.append(ScraperController())

if settings.features.enable_analytics:
    controllers.append(AnalyticsController())

# Always include core controllers
controllers.extend([
    ArticlesController(),
    AuthController(),
    LikesController(),
    HealthController(),
])

# Register routes with tags
app.include_router(controllers[0].router, prefix="/search", tags=["Search"])
app.include_router(controllers[1].router, prefix="/find", tags=["Recommendations"])
app.include_router(controllers[2].router, prefix="/scrape", tags=["Scraping"])
app.include_router(controllers[3].router, prefix="/analytics", tags=["Analytics"])
app.include_router(controllers[4].router, prefix="/articles", tags=["Articles"])
app.include_router(controllers[5].router, prefix="/auth", tags=["Authentication"])
app.include_router(controllers[6].router, prefix="/user", tags=["User Preferences"])
app.include_router(controllers[7].router, tags=["Health"])

# Configure Prometheus monitoring if enabled
if settings.monitoring.prometheus_enabled:
    Instrumentator().instrument(app).expose(app)

@app.get("/", 
    summary="API Root",
    description="Root endpoint that confirms the API is running and provides basic information.",
    response_description="API status and version information",
    tags=["Health"]
)
def root():
    """
    Root endpoint that confirms the API is running.
    
    Returns basic information about the API including version and status.
    """
    return {
        "message": f"{settings.app_name} is running ✅",
        "version": settings.app_version,
        "environment": get_environment(),
        "status": "healthy",
        "documentation": "/docs",
        "health_check": "/health",
        "features": {
            "search": settings.features.enable_search,
            "recommendations": settings.features.enable_recommendations,
            "scraping": settings.features.enable_scraping,
            "analytics": settings.features.enable_analytics,
        }
    }
