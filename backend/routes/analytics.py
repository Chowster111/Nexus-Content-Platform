from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from db.supabase_client import supabase
from logging_config import logger
from .utils.retry import with_backoff

router = APIRouter()

@with_backoff(max_retries=3, backoff_factor=0.5)
def fetch_articles():
    return supabase.table("articles").select("*").order("published_date", desc=True).execute()

@with_backoff(max_retries=3, backoff_factor=0.5)
def fetch_categories():
    return supabase.table("articles").select("category").execute()

# ---

@router.get("/blogs-by-source/{limit}")
def blogs_by_source(limit: int = 25):
    logger.info(f"📊 Fetching blogs by source with limit={limit}")
    try:
        response = fetch_articles()
    except Exception as e:
        logger.exception("❌ Failed to fetch articles for source analysis")
        raise HTTPException(status_code=500, detail=str(e))

    articles = response.data
    logger.info(f"📄 Retrieved {len(articles)} articles")

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

@router.get("/category-count")
def get_article_count_by_category():
    logger.info("📊 Fetching article count by category")
    try:
        result = fetch_categories()
    except Exception as e:
        logger.exception("❌ Failed to fetch categories")
        raise HTTPException(status_code=500, detail=str(e))

    category_counts = defaultdict(int)
    for row in result.data:
        cat = row.get("category", "Unknown")
        category_counts[cat] += 1

    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    logger.info(f"✅ Category counts: {sorted_categories}")

    return JSONResponse(
        content={"categories": sorted_categories},
        headers={"Cache-Control": "public, max-age=600"}
    )
