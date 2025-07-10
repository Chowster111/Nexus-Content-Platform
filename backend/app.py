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

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 FastAPI application is starting up")
    yield
    logger.info("🛑 FastAPI application is shutting down")

app = FastAPI(
    title="Engineering Blog Recommender API",
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
    version="1.0.0",
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

controllers = [
    SearchController(),       # 0
    ArticlesController(),     # 1
    ScraperController(),      # 2
    RecommendController(),    # 3
    AnalyticsController(),    # 4
    AuthController(),         # 5
    LikesController(),        # 6
    HealthController(),       # 7
]

app.include_router(controllers[0].router, prefix="/search", tags=["Search"])
app.include_router(controllers[1].router, prefix="/articles", tags=["Articles"])
app.include_router(controllers[2].router, prefix="/scrape", tags=["Scraping"])
app.include_router(controllers[3].router, prefix="/find", tags=["Recommendations"])
app.include_router(controllers[4].router, prefix="/analytics", tags=["Analytics"])
app.include_router(controllers[5].router, prefix="/auth", tags=["Authentication"])
app.include_router(controllers[6].router, prefix="/user", tags=["User Preferences"])
app.include_router(controllers[7].router, tags=["Health"])

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
        "message": "Engineering Blog Recommender API is running ✅",
        "version": "1.0.0",
        "status": "healthy",
        "documentation": "/docs",
        "health_check": "/health"
    }
