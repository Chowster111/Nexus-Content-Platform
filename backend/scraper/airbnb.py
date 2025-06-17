# airbnb.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time
from .utils.embedding_utils import safe_encode, classify_article_semantically, semantic_model, category_embeddings,kw_model

device = "cpu"
def scrape_all_airbnb_articles():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://medium.com/airbnb-engineering")

    SCROLL_PAUSE = 3
    MAX_SCROLLS = 30
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(MAX_SCROLLS):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")

    articles = []
    post_blocks = soup.select("div[data-post-id]")  # Updated selector

    print("🔍 Found:", len(post_blocks))

    for post in post_blocks:
        try:
            # Extract title
            title_el = post.select_one("h3 > div")
            title = title_el.get_text(strip=True) if title_el else None

            # Extract URL
            link_el = post.select_one("a[href*='airbnb-engineering']")
            url = link_el["href"].split("?")[0] if link_el else None

            # Extract date
            time_el = post.select_one("time")
            published_date = (
                datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
                if time_el and "datetime" in time_el.attrs else None
            )

            summary = ""  # Placeholder
            if title and url:
                text_for_tags = f"{title}. {summary}" if summary else title
                keywords = kw_model.extract_keywords(
                    text_for_tags, keyphrase_ngram_range=(1, 2),
                    stop_words='english', top_n=5
                )
                tags = [kw for kw, _ in keywords]
                category = classify_article_semantically(title, summary, category_embeddings, semantic_model)
                text_for_embedding = f"Title: {title}. Category: {category}. Tags: {', '.join(tags)} Airbnb Engineering Blog"
                embedding = safe_encode(text_for_embedding, semantic_model)
                if embedding is None:
                    print(f"⚠️ Skipping due to invalid embedding: {title}")
                    continue
                articles.append({
                    "title": title,
                    "url": url,
                    "published_date": published_date,
                    "source": "Airbnb Engineering Blog",
                    "tags": tags,
                    "category": category,
                    "embedding": embedding    
                })

        except Exception as e:
            print(f"⚠️ Skipping article due to error: {e}")
            continue

    return articles
