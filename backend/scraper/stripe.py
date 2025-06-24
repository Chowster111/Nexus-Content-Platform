# stripe_scraper.py
import time
from datetime import datetime

from bs4 import BeautifulSoup

from .baseScraper import BaseBlogScraper

device = "cpu"
class StripeScraper(BaseBlogScraper):
    def __init__(self):
        super().__init__(
            source_name="Stripe Blog",
            base_url="https://stripe.com/blog/page/1",  # Starting URL
            scroll_limit=0  # We’ll paginate manually
        )
        self.MAX_PAGES = 10

    def get_soup_pages(self):
        soups = []
        for page in range(1, self.MAX_PAGES + 1):
            print(f"🌐 Visiting page {page}")
            self.driver.get(f"https://stripe.com/blog/page/{page}")
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            soups.append(soup)
        self.driver.quit()
        return soups

    def select_posts(self, soup):
        return soup.select("article.BlogIndexPost")

    def parse_post(self, post):
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

        if title and url:
            return self.enrich_article(title, url, published_date, summary)
        return None

    def scrape(self):
        soups = self.get_soup_pages()
        articles = []

        for soup in soups:
            posts = self.select_posts(soup)
            for post in posts:
                try:
                    article = self.parse_post(post)
                    if article:
                        articles.append(article)
                except Exception as e:
                    print(f"⚠️ Error scraping post: {e}")
        return articles
