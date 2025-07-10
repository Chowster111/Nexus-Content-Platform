# stripe_scraper.py
import time
from datetime import datetime
from typing import List, Optional
from bs4 import BeautifulSoup, Tag

from .baseScraper import BaseBlogScraper
from ..models.models import ScrapedArticle

device = "cpu"


class StripeScraper(BaseBlogScraper):
    def __init__(self) -> None:
        super().__init__(
            source_name="Stripe Blog",
            base_url="https://stripe.com/blog/page/1",  # Starting URL
            scroll_limit=0  # We'll paginate manually
        )
        self.MAX_PAGES: int = 10

    def get_soup_pages(self) -> List[BeautifulSoup]:
        """Get BeautifulSoup objects from multiple pages."""
        soups: List[BeautifulSoup] = []
        for page in range(1, self.MAX_PAGES + 1):
            print(f"🌐 Visiting page {page}")
            self.driver.get(f"https://stripe.com/blog/page/{page}")
            time.sleep(3)
            soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, "html.parser")
            soups.append(soup)
        self.driver.quit()
        return soups

    def select_posts(self, soup: BeautifulSoup) -> List[Tag]:
        """Select post elements from the Stripe blog."""
        return soup.select("article.BlogIndexPost")

    def parse_post(self, post: Tag) -> Optional[ScrapedArticle]:
        """Parse a single Stripe post element."""
        title_el: Optional[Tag] = post.select_one(".BlogIndexPost__title a")
        title: Optional[str] = title_el.get_text(strip=True) if title_el else None
        url: Optional[str] = "https://stripe.com" + title_el["href"] if title_el else None

        date_el: Optional[Tag] = post.select_one("time")
        published_date: Optional[datetime] = (
            datetime.fromisoformat(date_el["datetime"])
            if date_el and date_el.has_attr("datetime") else None
        )

        summary_el: Optional[Tag] = post.select_one(".BlogIndexPost__body p")
        summary: str = summary_el.get_text(strip=True) if summary_el else ""

        if title and url:
            return self.enrich_article(title, url, published_date, summary)
        return None

    def scrape(self) -> List[ScrapedArticle]:
        """Main scraping method for Stripe articles."""
        soups: List[BeautifulSoup] = self.get_soup_pages()
        articles: List[ScrapedArticle] = []

        for soup in soups:
            posts: List[Tag] = self.select_posts(soup)
            for post in posts:
                try:
                    article: Optional[ScrapedArticle] = self.parse_post(post)
                    if article:
                        articles.append(article)
                except Exception as e:
                    print(f"⚠️ Error scraping post: {e}")
        return articles
