import time
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Union
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from pydantic import ValidationError

from .utils.embedding_utils import (
    category_embeddings,
    classify_article_semantically,
    kw_model,
    safe_encode,
    semantic_model,
)
from ..models.scraper import ScrapedArticle, ScraperConfig

device = "cpu"


class BaseBlogScraper(ABC):
    def __init__(self, source_name: str, base_url: str, scroll_limit: int = 30) -> None:
        self.source_name: str = source_name
        self.base_url: str = base_url
        self.scroll_limit: int = scroll_limit
        self.driver: WebDriver = self._init_driver()

    def _init_driver(self) -> WebDriver:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=chrome_options)

    @abstractmethod
    def scroll_page(self) -> None:
        """Scroll the page to load more content. Must be implemented by subclasses."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for _ in range(self.scroll_limit):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_soup(self) -> BeautifulSoup:
        """Get BeautifulSoup object from the page."""
        self.driver.get(self.base_url)
        self.scroll_page()
        html: str = self.driver.page_source
        self.driver.quit()
        # Validate scraped data if needed
        try:
            soup = BeautifulSoup(html, "html.parser")
            # Example: validate a dummy ScrapedArticle if you parse here
            # ScrapedArticle(title="Test", url="http://example.com", source=self.source_name, tags=[], category="General")
            return soup
        except ValidationError as ve:
            print(f"❌ Validation error in get_soup for {self.base_url}: {ve}")
            raise

    def parse_post(self, post: Tag) -> Optional[ScrapedArticle]:
        """Parse a single post element. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this")

    def scrape(self) -> List[ScrapedArticle]:
        """Main scraping method that returns a list of scraped articles."""
        soup: BeautifulSoup = self.get_soup()
        posts: List[Tag] = self.select_posts(soup)
        articles: List[ScrapedArticle] = []

        for post in posts:
            try:
                article: Optional[ScrapedArticle] = self.parse_post(post)
                if article:
                    articles.append(article)
            except Exception as e:
                print(f"⚠️ Error scraping post: {e}")
        return articles

    def select_posts(self, soup: BeautifulSoup) -> List[Tag]:
        """Select post elements from the soup. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this")

    def enrich_article(self, title: str, url: str, published_date: Optional[str], summary: str = "") -> Optional[ScrapedArticle]:
        """Enrich article with semantic analysis and embeddings."""
        text: str = f"{title}. {summary}" if summary else title
        keywords: List[tuple] = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
        tags: List[str] = [kw for kw, _ in keywords]
        category: str = classify_article_semantically(title, summary, category_embeddings, semantic_model)
        embedding: Optional[List[float]] = safe_encode(f"Title: {title}. Category: {category}. Tags: {', '.join(tags)} {self.source_name}", semantic_model)
        
        if embedding is None:
            return None
            
        return ScrapedArticle(
            title=title,
            url=url,
            published_date=published_date,
            source=self.source_name,
            tags=tags,
            category=category,
            embedding=embedding,
            summary=summary
        )
