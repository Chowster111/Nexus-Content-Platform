# tinder_scraper.py
from datetime import datetime
from typing import List, Optional
from bs4 import BeautifulSoup, Tag

from .baseScraper import BaseBlogScraper
from ..models.models import ScrapedArticle

device = "cpu"


class TinderScraper(BaseBlogScraper):
    def __init__(self) -> None:
        super().__init__(
            source_name="Tinder Tech Blog",
            base_url="https://medium.com/tinder",
            scroll_limit=30
        )

    def select_posts(self, soup: BeautifulSoup) -> List[Tag]:
        """Select post elements from the Tinder blog."""
        return soup.select("div[data-post-id]")

    def parse_post(self, post: Tag) -> Optional[ScrapedArticle]:
        """Parse a single Tinder post element."""
        title_el: Optional[Tag] = post.select_one("h3 > div")
        title: Optional[str] = title_el.get_text(strip=True) if title_el else None

        link_el: Optional[Tag] = post.select_one("a[href*='tinder']")
        url: Optional[str] = link_el["href"].split("?")[0] if link_el else None

        time_el: Optional[Tag] = post.select_one("time")
        published_date: Optional[datetime] = (
            datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
            if time_el and "datetime" in time_el.attrs else None
        )

        summary: str = ""
        if title and url:
            return self.enrich_article(title, url, published_date, summary)
        return None
