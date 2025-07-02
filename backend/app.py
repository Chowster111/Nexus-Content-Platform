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
    version="1.0.0",
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

app.include_router(controllers[0].router, prefix="/search")
app.include_router(controllers[1].router, prefix="/articles")
app.include_router(controllers[2].router, prefix="/scrape")
app.include_router(controllers[3].router, prefix="/find")
app.include_router(controllers[4].router, prefix="/analytics")
app.include_router(controllers[5].router, prefix="/auth")
app.include_router(controllers[6].router, prefix="/user")
app.include_router(controllers[7].router)

Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "Engineering Blog Recommender API is running ✅"}
