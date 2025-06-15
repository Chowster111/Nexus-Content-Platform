from db.supabase_client import supabase
import math

def is_valid_embedding(embedding, expected_dim=384):
    return (
        isinstance(embedding, list)
        and len(embedding) == expected_dim
        and all(isinstance(x, (float, int)) and math.isfinite(x) for x in embedding)
    )

def trigger_scrape(source_name: str, scrape_fn):
    articles = scrape_fn()
    print(f"\n🧠 Scraper returned {len(articles)} articles.")

    saved = 0

    for i, article in enumerate(articles):
        print(f"\n--- Article {i+1} ---")
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Published: {article['published_date']}")
        print(f"Content: {article.get('content', '')[:80]}...")

        embedding = article.get("embedding", None)
        if not is_valid_embedding(embedding):
            print("⚠️ Skipping article due to invalid embedding.")
            continue

        # Check for duplicates
        existing = supabase.table("articles").select("id").eq("url", article["url"]).execute()
        if existing.data:
            article_id = existing.data[0]['id']
            try:
                supabase.table("articles").update({
                    "embedding": embedding
                }).eq("id", article_id).execute()
                print("✅ Updated.")
                continue
            except Exception as e:
                print(f"❌ Update failed: {e}")
                continue

        # Insert new article
        try:
            result = supabase.table("articles").insert({
                "title": article["title"],
                "url": article["url"],
                "published_date": article["published_date"].isoformat() if article["published_date"] else None,
                "content": article.get("content", ""),
                "source": article.get("source", source_name),
                "tags": article.get("tags", []),
                "category": article.get("category", ""),
                "embedding": embedding
            }).execute()

            print(result.data)
            print("✅ Inserted.")
            saved += 1
        except Exception as e:
            print(f"❌ Insert failed: {e}")

    print(f"\n📦 Finished. {saved} new articles inserted.")
    return {"message": f"{saved} new articles scraped and saved from {source_name}."}
