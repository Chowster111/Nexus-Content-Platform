from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from .baseScraper import BaseBlogScraper


class DoorDashScraper(BaseBlogScraper):
    def __init__(self):
        super().__init__(
            source_name="DoorDash Engineering Blog",
            base_url="https://careersatdoordash.com/engineering-blog/",
            scroll_limit=0  # Will use click instead of scroll
        )
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_soup_pages(self):
        soups = []
        try:
            print(f"🌐 Visiting DoorDash Engineering Blog — {self.base_url}")
            self.driver.get(self.base_url)

            while True:
                # Wait for posts to load
                time.sleep(2)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                posts = self.select_posts(soup)
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

    def select_posts(self, soup):
        return soup.select("div.fade.h-full")

    def parse_post(self, post):
        a_tag = post.select_one("a")
        url = a_tag["href"] if a_tag else None

        title_el = post.select_one("p.with-tags")
        title = title_el.get_text(strip=True) if title_el else None

        tags = []
        tag_els = post.select("div.flex.items-center.flex-wrap div.bg-gray")
        for tag_el in tag_els:
            tag = tag_el.get_text(strip=True)
            if tag:
                tags.append(tag)

        if title and url:
            article = self.enrich_article(title, url, None, summary="")
            if tags:
                article["tags"] = tags
            return article

        print(f"⚠️ Missing title or URL for DoorDash post.")
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

        print(f"✅ Scraped {len(articles)} DoorDash posts.")
        return articles
