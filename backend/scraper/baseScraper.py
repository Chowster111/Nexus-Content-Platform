import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .utils.embedding_utils import (
    category_embeddings,
    classify_article_semantically,
    kw_model,
    safe_encode,
    semantic_model,
)

device = "cpu"
class BaseBlogScraper:
    def __init__(self, source_name, base_url, scroll_limit=30):
        self.source_name = source_name
        self.base_url = base_url
        self.scroll_limit = scroll_limit
        self.driver = self._init_driver()

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=chrome_options)

    def scroll_page(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for _ in range(self.scroll_limit):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_soup(self):
        self.driver.get(self.base_url)
        self.scroll_page()
        html = self.driver.page_source
        self.driver.quit()
        return BeautifulSoup(html, "html.parser")

    def parse_post(self, post):
        raise NotImplementedError("Subclasses must implement this")

    def scrape(self):
        soup = self.get_soup()
        posts = self.select_posts(soup)
        articles = []

        for post in posts:
            try:
                article = self.parse_post(post)
                if article:
                    articles.append(article)
            except Exception as e:
                print(f"⚠️ Error scraping post: {e}")
        return articles

    def select_posts(self, soup):
        raise NotImplementedError("Subclasses must implement this")

    def enrich_article(self, title, url, published_date, summary=""):
        text = f"{title}. {summary}" if summary else title
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
        tags = [kw for kw, _ in keywords]
        category = classify_article_semantically(title, summary, category_embeddings, semantic_model)
        embedding = safe_encode(f"Title: {title}. Category: {category}. Tags: {', '.join(tags)} {self.source_name}", semantic_model)
        if embedding is None:
            return None
        return {
            "title": title,
            "url": url,
            "published_date": published_date,
            "source": self.source_name,
            "tags": tags,
            "category": category,
            "embedding": embedding
        }
