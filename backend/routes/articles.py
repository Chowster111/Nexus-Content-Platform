from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException
from db.supabase_client import supabase
from logging_config import logger
from .utils.retry import with_backoff
from collections import defaultdict

class ArticlesController:
    def __init__(self):
        self.router = APIRouter()
        self.router.get("/")(self.get_all_articles)
        self.router.get("/tags/{tag}")(self.get_articles_by_tag)
        self.router.get("/filter")(self.filter_articles_by_tag)
        self.router.get("/all-tags")(self.get_all_tags)
        self.router.get("/by-category/{category}")(self.get_by_category)
        self.router.get("/by-source/{source}")(self.get_by_source)
        self.router.get("/{article_id}")(self.get_article)

    @with_backoff()
    def _fetch_articles(self):
        return supabase.table("articles").select("*").execute()

    @with_backoff()
    def _fetch_tags(self):
        return supabase.table("articles").select("tags").execute()

    def _sort_articles(self, articles, sort_order):
        return sorted(
            articles,
            key=lambda a: a.get("published_date", ""),
            reverse=(sort_order == "latest")
        )

    def get_all_articles(self):
        logger.info("Fetching all articles")
        try:
            response = supabase.table("articles").select("*").order("published_date", desc=True).execute()
            return response.data
        except Exception as e:
            logger.exception("ERROR fetching all articles")
            raise HTTPException(status_code=500, detail=str(e))

    def get_articles_by_tag(self, tag: str, sort: str = Query("latest", pattern="^(latest|oldest)$")):
        logger.info(f"Fetching articles by tag: '{tag}' with sort='{sort}'")
        tag = tag.lower()
        try:
            response = self._fetch_articles()
        except Exception as e:
            logger.exception("ERROR fetching articles by tag")
            raise HTTPException(status_code=500, detail=str(e))

        filtered = [
            a for a in response.data
            if a.get("tags") and any(tag in t.lower() for t in a["tags"])
        ]

        sorted_articles = self._sort_articles(filtered, sort)
        return sorted_articles

    def filter_articles_by_tag(self, tags: Optional[List[str]] = Query(None), sort: str = Query("latest", pattern="^(latest|oldest)$")):
        if not tags:
            raise HTTPException(status_code=400, detail="No tags provided")

        tags = [tag.lower() for tag in tags]
        logger.info(f"🔍 Filtering by tags: {tags} with sort='{sort}'")
        try:
            response = self._fetch_articles()
        except Exception as e:
            logger.exception("ERROR filtering articles by tag")
            raise HTTPException(status_code=500, detail=str(e))

        filtered = [
            a for a in response.data
            if a.get("tags") and any(
                any(query_tag in tag.lower() for tag in a["tags"])
                for query_tag in tags
            )
        ]

        return self._sort_articles(filtered, sort)

    def get_all_tags(self):
        logger.info("Fetching all tags")
        try:
            response = self._fetch_tags()
        except Exception as e:
            logger.exception("ERROR fetching all tags")
            raise HTTPException(status_code=500, detail=str(e))

        tag_counter = defaultdict(int)
        for row in response.data:
            for tag in row.get("tags", []):
                tag_counter[tag.lower()] += 1

        sorted_tags = sorted(tag_counter.items(), key=lambda x: -x[1])
        return [{"tag": tag, "count": count} for tag, count in sorted_tags]

    def get_by_category(self, category: str, sort: str = Query("latest", pattern="^(latest|oldest)$")):
        category = category[0].upper() + category[1:].lower()
        logger.info(f"Fetching articles by category: '{category}'")
        try:
            response = supabase.table("articles").select("*").eq("category", category).execute()
        except Exception as e:
            logger.exception("ERROR fetching by category")
            raise HTTPException(status_code=500, detail=str(e))

        return self._sort_articles(response.data, sort)

    def get_by_source(self, source: str, sort: str = Query("latest", pattern="^(latest|oldest)$")):
        source = source.lower()
        source = {
            "netflix": "Netflix Tech Blog",
            "airbnb": "Airbnb Engineering Blog",
            "stripe": "Stripe Blog",
            "tinder": "Tinder Tech Blog",
            "uber": "Uber Engineering Blog"
        }.get(source, source)

        logger.info(f"Fetching by source: '{source}'")
        try:
            response = supabase.table("articles").select("*").eq("source", source).execute()
        except Exception as e:
            logger.exception("ERROR fetching by source")
            raise HTTPException(status_code=500, detail=str(e))

        return self._sort_articles(response.data, sort)

    def get_article(self, article_id: str):
        logger.info(f"Fetching single article with id: {article_id}")
        try:
            response = supabase.table("articles").select("*").eq("id", article_id).single().execute()
            return response.data
        except Exception as e:
            logger.exception("ERROR fetching article")
            raise HTTPException(status_code=500, detail=str(e))
