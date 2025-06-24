from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analytics import router as analytics_router
from routes.articles import router as articles_router
from routes.auth import router as auth_router
from routes.likes import router as likes_router
from routes.recommend import router as recommend_router
from routes.scraper import router as scraper_router
from routes.search import router as search_router

app = FastAPI()
# CORS settings for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route groups
app.include_router(articles_router, prefix="/articles")
app.include_router(scraper_router, prefix="/scrape")
app.include_router(recommend_router, prefix="/find")
app.include_router(search_router, prefix="/search")
app.include_router(analytics_router, prefix="/analytics")
app.include_router(auth_router, prefix="/auth")
app.include_router(likes_router, prefix="/user")

@app.get("/")
def root():
    return {"message": "Engineering Blog Recommender API"}