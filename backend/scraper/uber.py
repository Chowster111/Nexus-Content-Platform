# uber.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time
from .utils.embedding_utils import safe_encode, classify_article_semantically, semantic_model, category_embeddings, kw_model

BASE_URL = "https://www.uber.com/en-CA/blog/engineering/page/{}"
MAX_PAGES = 2 # For testing, adjust as needed

device = "cpu"
def scrape_all_uber_articles():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    articles = []
    
    for page_num in range(1, MAX_PAGES + 1):
        print(f"\n🌐 Visiting page {page_num}...")
        driver.get(BASE_URL.format(page_num))
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        post_blocks = soup.select("div[data-baseweb='flex-grid-item']")

        if not post_blocks:
            print("❌ No more posts found. Stopping pagination.")
            break

        print(f"🔍 Found {len(post_blocks)} posts.")

        for post in post_blocks:
            try:
                title_el = post.select_one("h2")
                link_el = post.select_one("a[href]")
                date_el = post.select_one("p")

                title = title_el.get_text(strip=True) if title_el else None
                url = link_el["href"].split("?")[0] if link_el else None
                date_text = date_el.get_text(strip=True).split(" / ")[0] if date_el else None
                published_date = None
                if date_text:
                    try:
                        published_date = datetime.strptime(date_text, "%B %d, %Y")
                    except Exception as e:
                        print(f"⚠️ Date parse failed: {date_text} — {e}")



                summary = ""
                if title and url:
                    text_for_tags = f"{title}. {summary}" if summary else title
                    keywords = kw_model.extract_keywords(
                        text_for_tags, keyphrase_ngram_range=(1, 2),
                        stop_words='english', top_n=5
                    )
                    tags = [kw for kw, _ in keywords]
                    category = classify_article_semantically(title, summary, category_embeddings, semantic_model)
                    text_for_embedding = f"Title: {title}. Category: {category}. Tags: {', '.join(tags)} Uber Engineering Blog"
                    embedding = safe_encode(text_for_embedding, semantic_model)
                    if embedding is None:
                        print(f"⚠️ Skipping due to invalid embedding: {title}")
                        continue
                    articles.append({
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "source": "Uber Engineering Blog",
                        "tags": tags,
                        "category": category,
                        "embedding": embedding    
                    })

            except Exception as e:
                print(f"⚠️ Error scraping post: {e}")
                continue

    driver.quit()
    print(f"\n✅ Done. Total articles scraped: {len(articles)}")
    return articles
