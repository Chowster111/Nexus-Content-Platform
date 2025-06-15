from fastapi import APIRouter, Query
from typing import Optional, List
from db.supabase_client import supabase

router = APIRouter()

@router.get("/")
def get_all_articles():
    response = supabase.table("articles").select("*").order("published_date", desc=True).execute()
    return response.data

@router.get("/search")
def search_articles(query: str = Query(..., min_length=2)):
    response = (
        supabase.table("articles")
        .select("*")
        .ilike("title", f"%{query}%")
        .execute()
    )
    return response.data

@router.get("/tags/{tag}")
def get_articles_by_tag(tag: str, sort: str = Query("latest", pattern="^(latest|oldest)$")):
    tag = tag.lower()
    response = supabase.table("articles").select("*").execute()
    all_articles = response.data

    filtered_articles = [
        article for article in all_articles
        if article.get("tags") and any(tag in t.lower() for t in article["tags"])
    ]

    sorted_articles = sorted(
        filtered_articles,
        key=lambda a: a.get("published_date", ""),
        reverse=(sort == "latest")
    )
    return sorted_articles

@router.get("/filter")
def filter_articles_by_tag(
    tags: Optional[List[str]] = Query(None),
    sort: str = Query("latest", pattern="^(latest|oldest)$")
):
    if not tags:
        return {"error": "No tags provided"}

    tags = [tag.lower() for tag in tags]
    response = supabase.table("articles").select("*").execute()
    all_articles = response.data

    filtered_articles = [
        article for article in all_articles
        if article.get("tags") and any(
            any(query_tag in tag.lower() for tag in article["tags"])
            for query_tag in tags
        )
    ]

    sorted_articles = sorted(
        filtered_articles,
        key=lambda a: a.get("published_date", ""),
        reverse=(sort == "latest")
    )

    return sorted_articles

@router.get("/all-tags")
def get_all_tags():
    response = supabase.table("articles").select("tags").execute()
    tag_counter = {}

    for row in response.data:
        for tag in row.get("tags", []):
            tag_lower = tag.lower()
            tag_counter[tag_lower] = tag_counter.get(tag_lower, 0) + 1

    sorted_tags = sorted(tag_counter.items(), key=lambda x: -x[1])
    return [{"tag": tag, "count": count} for tag, count in sorted_tags]

@router.get("/by-category/{category}")
def get_by_category(category: str, sort: str = Query("latest", pattern="^(latest|oldest)$")):
    category = category[0].upper() + category[1:].lower()
    response = supabase.table("articles").select("*").eq("category", category).execute()
    all_articles = response.data

    sorted_articles = sorted(
        all_articles,
        key=lambda a: a.get("published_date", ""),
        reverse=(sort == "latest")
    )

    return sorted_articles

@router.get("/by-source/{source}")
def get_by_source(source: str, sort: str = Query("latest", pattern="^(latest|oldest)$")):

    source = "Netflix Tech Blog" if source.lower() == "netflix" else source
    source = "Airbnb Engineering Blog" if source.lower() == "airbnb" else source
    source = "Stripe Blog" if source.lower() == "stripe" else source
    source = "Tinder Tech Blog" if source.lower() == "tinder" else source

    response = supabase.table("articles").select("*").eq("source", source).execute()

    sorted_articles = sorted(
        response.data,
        key=lambda a: a.get("published_date", ""),
        reverse=(sort == "latest")
    )

    return sorted_articles

@router.get("/{article_id}")
def get_article(article_id: str):
    response = supabase.table("articles").select("*").eq("id", article_id).single().execute()
    return response.data
