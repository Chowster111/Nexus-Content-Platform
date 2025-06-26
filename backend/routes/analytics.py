from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Query
from db.supabase_client import supabase
from logging_config import logger

router = APIRouter()

@router.get("/blogs-by-source/{limit}")
def blogs_by_source(limit: int = 25):
    try:
        response = supabase.table("articles").select("*").order("published_date", desc=True).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    articles = response.data
    source_count = defaultdict(int)

    for article in articles:
        source = article.get("source", "Unknown")
        source_count[source] += 1

    sorted_sources = sorted(source_count.items(), key=lambda x: x[1], reverse=True)
    return {"sources": sorted_sources[:limit]}


@router.get("/tag-count")
def common_tags(limit: int = 10):
    try:
        response = supabase.table("articles").select("*").order("published_date", desc=True).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    articles = response.data
    tag_count = defaultdict(int)

    for article in articles:
        tags = article.get("tags") or []
        if isinstance(tags, str):  # handle comma-separated string
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        for tag in tags:
            tag_count[tag.lower()] += 1

    sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)
    return {"tags": sorted_tags[:limit]}


@router.get("/category-count")
def get_article_count_by_category():
    logger.info("Fetching article count by category")

    try:
        result = supabase.table("articles").select("category").execute()
    except Exception as e:
        logger.exception("❌ Failed to fetch categories")
        raise HTTPException(status_code=500, detail=str(e))

    category_counts = {}
    for row in result.data:
        cat = row["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    logger.info(f"✅ Category counts: {category_counts}")
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    return {"categories": sorted_categories}



@router.get("/blogs-by-source/{limit}")
def blogs_by_source(limit: int = 25):
    logger.info(f"📊 Fetching blogs by source with limit={limit}")

    try:
        response = supabase.table("articles").select("*").order("published_date", desc=True).execute()
    except Exception as e:
        logger.exception("❌ Failed to fetch articles for source analysis")
        raise HTTPException(status_code=500, detail=str(e))

    articles = response.data
    logger.info(f"📄 Retrieved {len(articles)} articles")

    source_count = {}
    for article in articles:
        source = article.get("source", "Unknown")
        source_count[source] = source_count.get(source, 0) + 1

    sorted_sources = sorted(source_count.items(), key=lambda x: x[1], reverse=True)
    logger.info(f"✅ Top sources: {sorted_sources[:limit]}")
    return {"sources": sorted_sources[:limit]}



@router.get("/most-recent/{topk}")
def get_most_recent(topk: int = 20):
    try:
        response = supabase.table("articles").select("*").order("published_date", desc=True).limit(topk).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    articles = response.data or []
    return [
        {
            "title": a.get("title"),
            "url": a.get("url"),
            "published_date": a.get("published_date"),
            "source": a.get("source", "Unknown"),
        }
        for a in articles
    ]


@router.get("/trending-tags")
def trending_tags(
    period: str = Query("month", enum=["week", "month", "year"]),
    top_n: int = 10
):
    now = datetime.utcnow()
    if period == "week":
        since = now - timedelta(weeks=1)
    elif period == "month":
        since = now - timedelta(days=30)
    elif period == "year":
        since = now - timedelta(days=365)

    try:
        response = supabase.table("articles").select("*").gte("published_date", since.isoformat()).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    tag_count = defaultdict(int)
    for article in response.data:
        tags = article.get("tags") or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        for tag in tags:
            tag_count[tag.lower()] += 1

    top_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return {"period": period, "top_tags": top_tags}
