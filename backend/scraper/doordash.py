from datetime import datetime
from typing import List, Optional
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
import time

from .baseScraper import BaseBlogScraper
from models.scraper import ScrapedArticle


class DoorDashScraper(BaseBlogScraper):
    def __init__(self) -> None:
        super().__init__(
            source_name="DoorDash Engineering Blog",
            base_url="https://careersatdoordash.com/engineering-blog/",
            scroll_limit=0  # Will use click instead of scroll
        )
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver: WebDriver = webdriver.Chrome(options=chrome_options)

    def get_soup_pages(self) -> List[BeautifulSoup]:
        """Get BeautifulSoup objects from multiple pages using load more button."""
        soups: List[BeautifulSoup] = []
        try:
            print(f"🌐 Visiting DoorDash Engineering Blog — {self.base_url}")
            self.driver.get(self.base_url)

            while True:
                # Wait for posts to load
                time.sleep(2)
                soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, "html.parser")
                posts: List[Tag] = self.select_posts(soup)
                soups.append(soup)

                # Try to click "See More"
                try:
                    load_more = self.driver.find_element("id", "load-more")
                    if load_more.is_displayed():
                        print("🔄 Clicking 'See More'...")
                        self.driver.execute_script("arguments[0].click();", load_more)
                        time.sleep(1)
                    else:
                        break
                except Exception:
                    print("✅ No more 'See More' button — finished loading.")
                    break

        finally:
            self.driver.quit()

        return soups

    def select_posts(self, soup: BeautifulSoup) -> List[Tag]:
        """Select post elements from the DoorDash blog."""
        return soup.select("div.fade.h-full")

    def parse_post(self, post: Tag) -> Optional[ScrapedArticle]:
        """Parse a single DoorDash post element."""
        a_tag: Optional[Tag] = post.select_one("a")
        url: Optional[str] = a_tag["href"] if a_tag else None

        title_el: Optional[Tag] = post.select_one("p.with-tags")
        title: Optional[str] = title_el.get_text(strip=True) if title_el else None

        tags: List[str] = []
        tag_els: List[Tag] = post.select("div.flex.items-center.flex-wrap div.bg-gray")
        for tag_el in tag_els:
            tag: str = tag_el.get_text(strip=True)
            if tag:
                tags.append(tag)

        if title and url:
            article: Optional[ScrapedArticle] = self.enrich_article(title, url, None, summary="")
            if article and tags:
                article.tags = tags
            return article

        print(f"⚠️ Missing title or URL for DoorDash post.")
        return None

    def scrape(self) -> List[ScrapedArticle]:
        """Main scraping method for DoorDash articles."""
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

        print(f"✅ Scraped {len(articles)} DoorDash posts.")
        return articles
