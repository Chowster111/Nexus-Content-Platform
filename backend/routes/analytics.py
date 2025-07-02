from collections import defaultdict
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from db.supabase_client import supabase
from logging_config import logger
from .utils.retry import with_backoff

class AnalyticsController:
    def __init__(self):
        self.router = APIRouter()
        self.register_routes()

    @staticmethod
    @with_backoff(max_retries=3, backoff_factor=0.5)
    def fetch_articles():
        logger.info("🔄 Fetching all articles from Supabase")
        return supabase.table("articles").select("*").order("published_date", desc=True).execute()

    @staticmethod
    @with_backoff(max_retries=3, backoff_factor=0.5)
    def fetch_categories():
        logger.info("🔄 Fetching article categories from Supabase")
        return supabase.table("articles").select("category").execute()

    def register_routes(self):
        @self.router.get("/blogs-by-source/{limit}")
        def blogs_by_source(limit: int = 25):
            logger.info(f"📊 Start: blogs-by-source | limit={limit}")
            try:
                response = self.fetch_articles()
            except Exception as e:
                logger.exception("❌ Error fetching articles for source count")
                raise HTTPException(status_code=500, detail=str(e))

            articles = response.data or []
            source_count = defaultdict(int)
            for article in articles:
                source = article.get("source", "Unknown")
                source_count[source] += 1

            sorted_sources = sorted(source_count.items(), key=lambda x: x[1], reverse=True)
            logger.info(f"✅ Top sources: {sorted_sources[:limit]}")

            return JSONResponse(
                content={"sources": sorted_sources[:limit]},
                headers={"Cache-Control": "public, max-age=600"}
            )

        @self.router.get("/category-count")
        def get_article_count_by_category():
            logger.info("📊 Start: category-count")
            try:
                result = self.fetch_categories()
            except Exception as e:
                logger.exception("❌ Error fetching categories")
                raise HTTPException(status_code=500, detail=str(e))

            category_counts = defaultdict(int)
            for row in result.data or []:
                category = row.get("category") or "Unknown"
                category_counts[category] += 1

            sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
            logger.info(f"✅ Category counts: {sorted_categories}")

            return JSONResponse(
                content={"categories": sorted_categories},
                headers={"Cache-Control": "public, max-age=600"}
            )
