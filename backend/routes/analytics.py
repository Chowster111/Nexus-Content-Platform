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
                logger.exception("ERROR fetching articles for source count")
                raise HTTPException(status_code=500, detail=str(e))

            articles = response.data or []
            source_count = defaultdict(int)
            for article in articles:
                source = article.get("source", "Unknown")
                source_count[source] += 1

            sorted_sources = sorted(source_count.items(), key=lambda x: x[1], reverse=True)
            logger.info(f"SUCCESS Top sources: {sorted_sources[:limit]}")

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
                logger.exception("ERROR fetching categories")
                raise HTTPException(status_code=500, detail=str(e))

            category_counts = defaultdict(int)
            for row in result.data or []:
                category = row.get("category") or "Unknown"
                category_counts[category] += 1

            sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
            logger.info(f"SUCCESS Category counts: {sorted_categories}")

            return JSONResponse(
                content={"categories": sorted_categories},
                headers={"Cache-Control": "public, max-age=600"}
            )

        @self.router.get("/top-liked-articles")
        def top_liked_articles():
            """Return the top 3 most liked articles."""
            logger.info("📊 Start: top-liked-articles")
            try:
                # Get all likes where liked is True
                likes_response = supabase.table("likes").select("article_url").eq("liked", True).execute()
                article_like_counts = defaultdict(int)
                for row in likes_response.data or []:
                    article_url = row.get("article_url")
                    if article_url:
                        article_like_counts[article_url] += 1
                # Get top 3 article URLs
                top_articles = sorted(article_like_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                # Fetch article details
                articles = []
                for url, count in top_articles:
                    article_resp = supabase.table("articles").select("title, url, summary, source, category, published_date").eq("url", url).single().execute()
                    if article_resp.data:
                        article = article_resp.data
                        article["like_count"] = count
                        articles.append(article)
                logger.info(f"SUCCESS Top liked articles: {articles}")
                return JSONResponse(content={"top_liked_articles": articles}, headers={"Cache-Control": "public, max-age=600"})
            except Exception as e:
                logger.exception("ERROR fetching top liked articles")
                raise HTTPException(status_code=500, detail=str(e))

        @self.router.get("/top-liked-categories")
        def top_liked_categories():
            """Return the top 3 most liked categories (by sum of likes on articles in that category)."""
            logger.info("📊 Start: top-liked-categories")
            try:
                # Get all likes where liked is True
                likes_response = supabase.table("likes").select("article_url").eq("liked", True).execute()
                article_like_counts = defaultdict(int)
                for row in likes_response.data or []:
                    article_url = row.get("article_url")
                    if article_url:
                        article_like_counts[article_url] += 1
                # Map article_url to category
                category_like_counts = defaultdict(int)
                for url, count in article_like_counts.items():
                    article_resp = supabase.table("articles").select("category").eq("url", url).single().execute()
                    category = article_resp.data.get("category") if article_resp.data else None
                    if category:
                        category_like_counts[category] += count
                # Get top 3 categories
                top_categories = sorted(category_like_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                logger.info(f"SUCCESS Top liked categories: {top_categories}")
                return JSONResponse(content={"top_liked_categories": top_categories}, headers={"Cache-Control": "public, max-age=600"})
            except Exception as e:
                logger.exception("ERROR fetching top liked categories")
                raise HTTPException(status_code=500, detail=str(e))
