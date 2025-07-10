from datetime import datetime
from typing import List, Optional
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
import time

from .baseScraper import BaseBlogScraper
from ..models.scraper import ScrapedArticle


class MetaEngineeringScraper(BaseBlogScraper):
    def __init__(self) -> None:
        super().__init__(
            source_name="Meta Engineering Blog",
            base_url="https://engineering.fb.com/",
            scroll_limit=0  # Using button click
        )
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver: WebDriver = webdriver.Chrome(options=chrome_options)

    def get_soup_pages(self) -> List[BeautifulSoup]:
        """Get BeautifulSoup objects from multiple pages using load more button."""
        soups: List[BeautifulSoup] = []
        click_count: int = 0
        MAX_CLICKS: int = 30 

        try:
            print(f"🌐 Visiting Meta Engineering Blog — {self.base_url}")
            self.driver.get(self.base_url)

            while click_count < MAX_CLICKS:
                time.sleep(2)
                soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, "html.parser")
                soups.append(soup)

                try:
                    load_more = self.driver.find_element("css selector", "button.loadmore-btn")
                    if load_more.is_displayed():
                        print(f"🔄 Clicking 'Load More'... ({click_count + 1}/{MAX_CLICKS})")
                        self.driver.execute_script("arguments[0].click();", load_more)
                        click_count += 1
                        time.sleep(2)
                    else:
                        print("✅ 'Load More' not displayed — stopping.")
                        break
                except Exception:
                    print("✅ No 'Load More' button found — done.")
                    break

            if click_count >= MAX_CLICKS:
                print(f"⏹️ Reached max clicks ({MAX_CLICKS}) — stopping.")

        finally:
            self.driver.quit()
        return soups

    def select_posts(self, soup: BeautifulSoup) -> List[Tag]:
        """Select post elements from the Meta blog."""
        return soup.select("article.post")

    def parse_post(self, post: Tag) -> Optional[ScrapedArticle]:
        """Parse a single Meta post element."""
        a_tag: Optional[Tag] = post.select_one(".entry-title a")
        url: Optional[str] = a_tag["href"] if a_tag else None
        title: Optional[str] = a_tag.get_text(strip=True) if a_tag else None

        tag_els: List[Tag] = post.select("span.cat-links a.category")
        tags: List[str] = [t.get_text(strip=True) for t in tag_els]

        published_date: Optional[datetime] = None

        if title and url:
            article: Optional[ScrapedArticle] = self.enrich_article(title, url, published_date, summary="")
            if article and tags:
                article.tags = tags
            return article

        print(f"⚠️ Missing title or URL for Meta post.")
        return None

    def scrape(self) -> List[ScrapedArticle]:
        """Main scraping method for Meta Engineering articles."""
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

        print(f"✅ Scraped {len(articles)} Meta Engineering posts.")
        return articles
