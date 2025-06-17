# stripe.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time
from .utils.embedding_utils import safe_encode, classify_article_semantically, semantic_model, category_embeddings,kw_model

device = "cpu"
def scrape_all_stripe_articles():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    base_url = "https://stripe.com/blog/page/"
    MAX_PAGES = 10
    articles = []

    for page in range(1, MAX_PAGES + 1):
        print(f"\n🌐 Visiting {base_url}{page}")
        driver.get(f"{base_url}{page}")
        time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        post_blocks = soup.select("article.BlogIndexPost")
        print(f"📄 Page {page}: Found {len(post_blocks)} posts")

        for post in post_blocks:
            try:
                title_el = post.select_one(".BlogIndexPost__title a")
                title = title_el.get_text(strip=True) if title_el else None
                url = "https://stripe.com" + title_el["href"] if title_el else None

                date_el = post.select_one("time")
                published_date = (
                    datetime.fromisoformat(date_el["datetime"])
                    if date_el and date_el.has_attr("datetime") else None
                )

                summary_el = post.select_one(".BlogIndexPost__body p")
                summary = summary_el.get_text(strip=True) if summary_el else ""

                text_for_tags = f"{title}. {summary}" if summary else title
                keywords = kw_model.extract_keywords(
                    text_for_tags, keyphrase_ngram_range=(1, 2),
                    stop_words='english', top_n=5
                )
                tags = [kw for kw, _ in keywords]
                category = classify_article_semantically(title, summary, category_embeddings, semantic_model)

                text_for_embedding = f"Title: {title}. Category: {category}. Tags: {', '.join(tags)} Stripe Blog"
                embedding = safe_encode(text_for_embedding, semantic_model)
                if embedding is None:
                    print(f"⚠️ Skipping due to invalid embedding: {title}")
                    continue

                articles.append({
                    "title": title,
                    "url": url,
                    "published_date": published_date,
                    "source": "Stripe Blog",
                    "tags": tags,
                    "category": category,
                    "embedding": embedding
                })

            except Exception as e:
                print(f"⚠️ Error parsing post: {e}")

    driver.quit()
    return articles
