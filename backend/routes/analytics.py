from collections import defaultdict
from typing import List, Dict, Any, Tuple, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from db.supabase_client import supabase
from logging_config import logger
from .utils.retry import with_backoff
from pydantic import ValidationError


class AnalyticsController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.register_routes()

    @staticmethod
    @with_backoff(max_retries=3, backoff_factor=0.5)
    def fetch_articles() -> Dict[str, Any]:
        """Fetch all articles from Supabase."""
        logger.info("🔄 Fetching all articles from Supabase")
        return supabase.table("articles").select("*").order("published_date", desc=True).execute()

    @staticmethod
    @with_backoff(max_retries=3, backoff_factor=0.5)
    def fetch_categories() -> Dict[str, Any]:
        """Fetch article categories from Supabase."""
        logger.info("🔄 Fetching article categories from Supabase")
        return supabase.table("articles").select("category").execute()

    def register_routes(self) -> None:
        """Register all analytics routes."""
        @self.router.get("/blogs-by-source/{limit}")
        def blogs_by_source(limit: int = 25) -> JSONResponse:
            """Get blogs grouped by source with counts."""
            logger.info(f"📊 Start: blogs-by-source | limit={limit}")
            try:
                response: Dict[str, Any] = self.fetch_articles()
            except Exception as e:
                logger.exception("ERROR fetching articles for source count")
                raise HTTPException(status_code=500, detail=str(e))

            articles: List[Dict[str, Any]] = response.data or []
            if not isinstance(articles, list):
                logger.error(f"Expected list for articles, got {type(articles)}: {articles}")
                raise HTTPException(status_code=500, detail="Internal error: articles data is not a list")
            source_count: Dict[str, int] = defaultdict(int)
            for article in articles:
                if not isinstance(article, dict):
                    logger.error(f"Expected dict for article, got {type(article)}: {article}")
                    continue
                source: str = article.get("source", "Unknown")
                source_count[source] += 1

            sorted_sources: List[Tuple[str, int]] = sorted(source_count.items(), key=lambda x: x[1], reverse=True)
            logger.info(f"SUCCESS Top sources: {sorted_sources[:limit]}")

            return JSONResponse(
                content={"sources": sorted_sources[:limit]},
                headers={"Cache-Control": "public, max-age=600"}
            )

        @self.router.get("/category-count")
        def get_article_count_by_category() -> JSONResponse:
            """Get article count by category."""
            logger.info("📊 Start: category-count")
            try:
                result: Dict[str, Any] = self.fetch_categories()
            except Exception as e:
                logger.exception("ERROR fetching categories")
                raise HTTPException(status_code=500, detail=str(e))

            category_counts: Dict[str, int] = defaultdict(int)
            for row in result.data or []:
                category: str = row.get("category") or "Unknown"
                category_counts[category] += 1

            sorted_categories: List[Tuple[str, int]] = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
            logger.info(f"SUCCESS Category counts: {sorted_categories}")

            return JSONResponse(
                content={"categories": sorted_categories},
                headers={"Cache-Control": "public, max-age=600"}
            )

        @self.router.get("/top-liked-articles")
        def top_liked_articles() -> JSONResponse:
            """Return the top 3 most liked articles."""
            logger.info("📊 Start: top-liked-articles")
            try:
                # Get all likes where liked is True
                likes_response: Dict[str, Any] = supabase.table("likes").select("article_url").eq("liked", True).execute()
                article_like_counts: Dict[str, int] = defaultdict(int)
                for row in likes_response.data or []:
                    article_url: Optional[str] = row.get("article_url")
                    if article_url:
                        article_like_counts[article_url] += 1
                # Get top 3 article URLs
                top_articles: List[Tuple[str, int]] = sorted(article_like_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                # Fetch article details
                articles: List[Dict[str, Any]] = []
                errors = []
                for url, count in top_articles:
                    article_resp: Dict[str, Any] = supabase.table("articles").select("title, url, summary, source, category, published_date").eq("url", url).single().execute()
                    if article_resp.data:
                        article: Dict[str, Any] = article_resp.data
                        article["like_count"] = count
                        try:
                            articles.append(article)
                        except ValidationError as ve:
                            logger.error(f"Validation error for top liked article: {article} | {ve}")
                            errors.append({"article": article, "error": str(ve)})
                if errors:
                    logger.warning(f"Some top liked articles could not be validated: {errors}")
                logger.info(f"SUCCESS Top liked articles: {articles}")
                return JSONResponse(content={"top_liked_articles": articles}, headers={"Cache-Control": "public, max-age=600"})
            except Exception as e:
                logger.exception("ERROR fetching top liked articles")
                raise HTTPException(status_code=500, detail=str(e))

        @self.router.get("/top-liked-categories")
        def top_liked_categories() -> JSONResponse:
            """Return the top 3 most liked categories (by sum of likes on articles in that category)."""
            logger.info("📊 Start: top-liked-categories")
            try:
                # Get all likes where liked is True
                likes_response: Dict[str, Any] = supabase.table("likes").select("article_url").eq("liked", True).execute()
                article_like_counts: Dict[str, int] = defaultdict(int)
                for row in likes_response.data or []:
                    article_url: Optional[str] = row.get("article_url")
                    if article_url:
                        article_like_counts[article_url] += 1
                # Map article_url to category
                category_like_counts: Dict[str, int] = defaultdict(int)
                for url, count in article_like_counts.items():
                    article_resp: Dict[str, Any] = supabase.table("articles").select("category").eq("url", url).single().execute()
                    category: Optional[str] = article_resp.data.get("category") if article_resp.data else None
                    if category:
                        category_like_counts[category] += count
                # Get top 3 categories
                top_categories: List[Tuple[str, int]] = sorted(category_like_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                logger.info(f"SUCCESS Top liked categories: {top_categories}")
                return JSONResponse(content={"top_liked_categories": top_categories}, headers={"Cache-Control": "public, max-age=600"})
            except Exception as e:
                logger.exception("ERROR fetching top liked categories")
                raise HTTPException(status_code=500, detail=str(e))
