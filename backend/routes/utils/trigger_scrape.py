import math

from db.supabase_client import supabase
from engine.summary import summarize
from scraper.airbnb import AirbnbScraper
from scraper.netflix import NetflixScraper
from scraper.stripe import StripeScraper
from scraper.tinder import TinderScraper
from scraper.uber import UberScraper
from scraper.notion import NotionScraper
from scraper.slack import SlackScraper
from scraper.robinhood import RobinhoodScraper
from scraper.doordash import DoorDashScraper
from scraper.meta import MetaEngineeringScraper
from pydantic import ValidationError
from models.models import ScrapedArticle

SCRAPER_MAP = {
    "netflix": NetflixScraper,
    "tinder": TinderScraper,
    "airbnb": AirbnbScraper,
    "uber": UberScraper,
    "stripe": StripeScraper,
    "notion": NotionScraper,
    "slack": SlackScraper,
    "robinhood": RobinhoodScraper,
    "doordash": DoorDashScraper,
    "meta" : MetaEngineeringScraper,
}


def is_valid_embedding(embedding, expected_dim=768):
    return (
        isinstance(embedding, list)
        and len(embedding) == expected_dim
        and all(isinstance(x, (float, int)) and math.isfinite(x) for x in embedding)
    )

def trigger_scrape(source_name: str, scrape_fn):
    articles = scrape_fn()
    print(f"\nScraper returned {len(articles)} articles.")

    saved = 0
    errors = []

    for i, article in enumerate(articles):
        print(f"\n--- Article {i+1} ---")
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Published: {article['published_date']}")
        print(f"Content: {article.get('content', '')[:80]}...")

        embedding = article.get("embedding", None)

        # Validate article structure
        try:
            ScrapedArticle(**article)
        except ValidationError as ve:
            print(f"❌ Validation error for scraped article: {article} | {ve}")
            errors.append({"article": article, "error": str(ve)})
            continue

        existing = supabase.table("articles").select("id").eq("url", article["url"]).execute()
        if existing.data:
            article_id = existing.data[0]['id']
            try:
                supabase.table("articles").update({
                    "content": "Content Coming..."
                }).eq("id", article_id).execute()
                print("✅ Updated Content.")
                continue
            except Exception as e:
                print(f"Update failed: {e}")
                continue

        # Insert new article
        try:
            result = supabase.table("articles").insert({
                "title": article["title"],
                "url": article["url"],
                "published_date": article["published_date"].isoformat() if article["published_date"] else None,
                "content": article.get("content", ""),
                "summary": summarize(article["title"], article["tags"]),
                "source": article.get("source", source_name),
                "tags": article.get("tags", []),
                "category": article.get("category", ""),
                "embedding": embedding
            }).execute()

            print(result.data)
            print("✅ Inserted.")
            saved += 1
        except Exception as e:
            print(f"Insert failed: {e}")

    if errors:
        print(f"⚠️ Some scraped articles failed validation: {errors}")

    print(f"\nFinished. {saved} new articles inserted.")
    return {"message": f"{saved} new articles scraped and saved from {source_name}."}
