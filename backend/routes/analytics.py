# analytics.py
from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Query

from db.supabase_client import supabase

router = APIRouter()

@router.get("/blogs-by-source/{limit}")
def blogs_by_source(limit: int = 25):
    try:
        response = supabase.table("articles").select("*").order("published_date", desc=True).execute()
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    articles = response.data
    source_count = {}

    for article in articles:
        source = article.get("source", "Unknown")
        source_count[source] = source_count.get(source, 0) + 1

    sorted_sources = sorted(source_count.items(), key=lambda x: x[1], reverse=True)
    return {"sources": sorted_sources[:limit]}


@router.get("/most-common-tags/{limit}")
def common_tags(limit: int = 10):
    try:
        response = supabase.table("articles").select("*").order("published_date", desc=True).execute()
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    articles = response.data
    tag_count = {}

    for article in articles:
        tags = article.get("tags", [])
        for tag in tags:
            tag = tag.lower()
            tag_count[tag] = tag_count.get(tag, 0) + 1

    sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)
    return {"tags": sorted_tags[:limit]}


@router.get("/category-count")
def get_article_count_by_category():
    try:
        result = supabase.table("articles").select("category").execute()
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    category_counts = {}
    for row in result.data:
        cat = row["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    return {"category_counts": category_counts}


@router.get("/articles-by-month")
def get_articles_by_month():
    try:
        response = supabase.table("articles").select("published_date").execute()
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    monthly_counts = defaultdict(int)

    for row in response.data:
        if row["published_date"]:
            dt = datetime.fromisoformat(row["published_date"])
            key = dt.strftime("%Y-%m")  # Format: "2025-06"
            monthly_counts[key] += 1

    return dict(sorted(monthly_counts.items()))


@router.get("/most-recent/{topk}")
def get_most_recent(topk: int = 20):
    try:
        response = supabase.table("articles").select("*").order("published_date", desc=True).execute()
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    topk = min(topk, len(response.data))
    articles = response.data[:topk]

    return [
        {
            "title": article["title"],
            "url": article["url"],
            "published_date": article["published_date"],
            "source": article["source"]
        }
        for article in articles
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
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    tag_count = {}
    for article in response.data:
        tags = article.get("tags", [])
        for tag in tags:
            tag = tag.lower()
            tag_count[tag] = tag_count.get(tag, 0) + 1

    top_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return {"period": period, "top_tags": top_tags}
