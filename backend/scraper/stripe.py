# stripe.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util
import torch
import math

CATEGORIES = {
    "Frontend": [
        "Responsive UI design", "JavaScript and CSS", "React components", "user interface engineering"
    ],
    "Backend": [
        "API development", "server-side logic", "database design", "backend scalability"
    ],
    "Infrastructure": [
        "DevOps practices", "Kubernetes", "CI/CD pipelines", "monitoring systems"
    ],
    "Machine Learning": [
        "ML pipelines", "deep learning", "recommendation systems", "NLP"
    ],
    "Security": [
        "application security", "OAuth", "encryption", "threat detection"
    ],
    "Cloud": [
        "AWS Lambda", "serverless architecture", "cloud computing", "Azure integration"
    ]
}

def is_valid_embedding(embedding, expected_dim=384):
    return (
        isinstance(embedding, list)
        and len(embedding) == expected_dim
        and all(isinstance(x, (float, int)) and math.isfinite(x) for x in embedding)
    )

kw_model = KeyBERT()
semantic_model = SentenceTransformer("BAAI/bge-base-en-v1.5")
category_embeddings = {
    cat: semantic_model.encode(examples, convert_to_tensor=True)
    for cat, examples in CATEGORIES.items()
}

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
                category = classify_article_semantically(title, summary)

                text_for_embedding = f"Title: {title}. Category: {category}. Tags: {', '.join(tags)} Stripe Blog"
                embedding = semantic_model.encode(text_for_embedding).tolist()  # convert to list for JSON/SQL insert
                if not is_valid_embedding(embedding):
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
