# uber_scraper.py
from datetime import datetime
from typing import List, Optional
from bs4 import BeautifulSoup, Tag

from .baseScraper import BaseBlogScraper
from ..models.scraper import ScrapedArticle

device = "cpu"


class UberScraper(BaseBlogScraper):
    def __init__(self) -> None:
        super().__init__(
            source_name="Uber Engineering Blog",
            base_url="https://www.uber.com/en-CA/blog/engineering/page/1",
            scroll_limit=2
        )
        self.MAX_PAGES: int = 40
        self.PAGE_TEMPLATE: str = "https://www.uber.com/en-CA/blog/engineering/page/{}"

    def get_soup_pages(self) -> List[BeautifulSoup]:
        """Get BeautifulSoup objects from multiple pages."""
        soups: List[BeautifulSoup] = []
        for page in range(1, self.MAX_PAGES + 1):
            print(f"\n🌐 Visiting Uber page {page}")
            self.driver.get(self.PAGE_TEMPLATE.format(page))
            self.driver.implicitly_wait(5)
            soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, "html.parser")
            soups.append(soup)
        self.driver.quit()
        return soups

    def select_posts(self, soup: BeautifulSoup) -> List[Tag]:
        """Select post elements from the Uber blog."""
        return soup.select("div[data-baseweb='flex-grid-item']")

    def parse_post(self, post: Tag) -> Optional[ScrapedArticle]:
        """Parse a single Uber post element."""
        title_el: Optional[Tag] = post.select_one("h2")
        link_el: Optional[Tag] = post.select_one("a[href]")
        date_el: Optional[Tag] = post.select_one("p")

        title: Optional[str] = title_el.get_text(strip=True) if title_el else None
        url: Optional[str] = None
        if link_el:
            url_path: str = link_el["href"].split("?")[0]
            url = "https://www.uber.com" + url_path

        date_text: Optional[str] = date_el.get_text(strip=True).split(" / ")[0] if date_el else None
        published_date: Optional[datetime] = None
        if date_text:
            try:
                published_date = datetime.strptime(date_text, "%B %d, %Y")
            except Exception as e:
                print(f"⚠️ Date parse failed: {date_text} — {e}")

        if title and url:
            return self.enrich_article(title, url, published_date, summary="")

        return None

    def scrape(self) -> List[ScrapedArticle]:
        """Main scraping method for Uber articles."""
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
