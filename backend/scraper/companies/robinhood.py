from datetime import datetime
from typing import List, Optional
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from ..base.base_scraper import BaseBlogScraper
from models.scraper import ScrapedArticle


class RobinhoodScraper(BaseBlogScraper):
    def __init__(self) -> None:
        super().__init__(
            source_name="Robinhood Newsroom",
            base_url="https://newsroom.aboutrobinhood.com/page/1/",
            scroll_limit=0
        )
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver: WebDriver = webdriver.Chrome(options=chrome_options)

        self.MAX_PAGES: int = 40

    def get_soup_pages(self) -> List[BeautifulSoup]:
        """Get BeautifulSoup objects from multiple pages."""
        soups: List[BeautifulSoup] = []
        try:
            for page in range(1, self.MAX_PAGES + 1):
                url: str = f"https://newsroom.aboutrobinhood.com/page/{page}/"
                print(f"🌐 Visiting Robinhood Newsroom page {page} — {url}")
                self.driver.get(url)
                soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, "html.parser")

                posts: List[Tag] = self.select_posts(soup)
                if not posts:
                    print(f"✅ No posts found on page {page} — stopping.")
                    break

                soups.append(soup)
        finally:
            self.driver.quit()
        return soups

    def select_posts(self, soup: BeautifulSoup) -> List[Tag]:
        """Select post elements from the soup."""
        return soup.select("div.frontpage-post-box")

    def parse_post(self, post: Tag) -> Optional[ScrapedArticle]:
        """Parse a single Robinhood post element."""
        # Title & URL
        title_el: Optional[Tag] = post.select_one("div.frontpage-post-title h2")
        title: Optional[str] = title_el.get_text(strip=True) if title_el else None

        link_el: Optional[Tag] = post.select_one("div.frontpage-post-title a")
        url: Optional[str] = link_el["href"] if link_el else None

        # Category tag
        cat_el: Optional[Tag] = post.select_one("div.frontpage-post-category span.post-category")
        tags: List[str] = []
        if cat_el:
            cat_text: str = cat_el.get_text(strip=True)
            if cat_text:
                tags.append(cat_text)

        # Published date
        date_el: Optional[Tag] = post.select_one("time.entry-date")
        published_date: Optional[datetime] = None
        if date_el and date_el.has_attr("datetime"):
            try:
                published_date = datetime.fromisoformat(date_el["datetime"])
            except Exception as e:
                print(f"⚠️ Date parse failed: {e}")

        # Summary/excerpt
        summary_el: Optional[Tag] = post.select_one("div.frontpage-post-excerpt p")
        summary: str = summary_el.get_text(strip=True) if summary_el else ""

        if title and url:
            article: Optional[ScrapedArticle] = self.enrich_article(title, url, published_date, summary)
            if article and tags:
                article.tags = tags
            return article

        print(f"⚠️ Missing title or URL for Robinhood post.")
        return None

    def scrape(self) -> List[ScrapedArticle]:
        """Main scraping method for Robinhood articles."""
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

        print(f"✅ Scraped {len(articles)} Robinhood posts.")
        return articles
