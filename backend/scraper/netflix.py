from datetime import datetime
from typing import List, Optional
from bs4 import BeautifulSoup, Tag

from .baseScraper import BaseBlogScraper
from ..models.models import ScrapedArticle

device = "cpu"


class NetflixScraper(BaseBlogScraper):
    def __init__(self) -> None:
        super().__init__("Netflix Tech Blog", "https://netflixtechblog.com", scroll_limit=50)

    def select_posts(self, soup: BeautifulSoup) -> List[Tag]:
        """Select post elements from the Netflix blog."""
        return soup.select("div.col.u-xs-size12of12.js-trackPostPresentation")

    def parse_post(self, post: Tag) -> Optional[ScrapedArticle]:
        """Parse a single Netflix post element."""
        title_el: Optional[Tag] = post.select_one("h3 > div")
        link_el: Optional[Tag] = post.select_one("a[href]")
        time_el: Optional[Tag] = post.select_one("time")

        title: Optional[str] = title_el.get_text(strip=True) if title_el else None
        url: Optional[str] = link_el["href"] if link_el else None
        published_date: Optional[datetime] = (
            datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
            if time_el else None
        )

        if title and url:
            return self.enrich_article(title, url, published_date)
        return None
