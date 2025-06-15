# tinder.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util
import time
from .constants import CATEGORIES
import math
kw_model = KeyBERT()
semantic_model = SentenceTransformer("BAAI/bge-base-en-v1.5")

category_embeddings = {
    cat: semantic_model.encode(examples, convert_to_tensor=True)
    for cat, examples in CATEGORIES.items()
}

def is_valid_embedding(embedding, expected_dim=384):
    return (
        isinstance(embedding, list)
        and len(embedding) == expected_dim
        and all(isinstance(x, (float, int)) and math.isfinite(x) for x in embedding)
    )


def classify_article_semantically(title: str, summary: str) -> str:
    text = f"{title}. {summary or ''}"
    emb = semantic_model.encode(text, convert_to_tensor=True)

    best_cat = "Uncategorized"
    best_score = -1

    for cat, reps in category_embeddings.items():
        sim = util.cos_sim(emb, reps).max().item()
        if sim > best_score:
            best_cat = cat
            best_score = sim

    return best_cat

def scrape_all_tinder_articles():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://medium.com/tinder")

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
            link_el = post.select_one("a[href*='tinder']")
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
                category = classify_article_semantically(title, summary)
                text_for_embedding = f"Title: {title}. Category: {category}. Tags: {', '.join(tags)} Tinder Tech Blog"
                embedding = semantic_model.encode(text_for_embedding).tolist()  # convert to list for JSON/SQL insert
                if not is_valid_embedding(embedding):
                    print(f"⚠️ Skipping due to invalid embedding: {title}")
                    continue
                articles.append({
                    "title": title,
                    "url": url,
                    "published_date": published_date,
                    "source": "Tinder Tech Blog",
                    "tags": tags,
                    "category": category,
                    "embedding": embedding    
                })

        except Exception as e:
            print(f"⚠️ Skipping article due to error: {e}")
            continue

    return articles
