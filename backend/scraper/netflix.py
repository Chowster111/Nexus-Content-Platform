# netflix.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time
from .utils.embedding_utils import safe_encode, classify_article_semantically, semantic_model, category_embeddings,kw_model

device = "cpu"
def scrape_all_netflix_articles():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://netflixtechblog.com")

    SCROLL_PAUSE = 3
    MAX_SCROLLS = 50

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
    post_blocks = soup.select("div.col.u-xs-size12of12.js-trackPostPresentation")
    print("🔍 Total post containers found:", len(post_blocks))

    articles = []
    for post in post_blocks:
        try:
            title_el = post.select_one("h3 > div")
            link_el = post.select_one("a[href]")
            time_el = post.select_one("time")

            title = title_el.get_text(strip=True) if title_el else None
            url = link_el["href"] if link_el else None
            published_date = (
                datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
                if time_el else None
            )

            summary = ""  # Placeholder for future content scraping

            if title and url:
                # Keyword + Category
                text_for_tags = f"{title}. {summary}" if summary else title
                keywords = kw_model.extract_keywords(
                    text_for_tags, keyphrase_ngram_range=(1, 2),
                    stop_words='english', top_n=5
                )
                tags = [kw for kw, _ in keywords]
                category = classify_article_semantically(title, summary, category_embeddings, semantic_model)

                # Embedding
                text_for_embedding = f"Title: {title}. Category: {category}. Tags: {', '.join(tags)} Netflix Tech Blog"
                embedding = safe_encode(text_for_embedding, semantic_model)
                if embedding is None:
                    print(f"⚠️ Skipping due to invalid embedding: {title}")
                    continue

                articles.append({
                    "title": title,
                    "url": url,
                    "published_date": published_date,
                    "source": "Netflix Tech Blog",
                    "tags": tags,
                    "category": category,
                    "embedding": embedding
                })

        except Exception as e:
            print(f"⚠️ Error scraping post: {e}")

    return articles
