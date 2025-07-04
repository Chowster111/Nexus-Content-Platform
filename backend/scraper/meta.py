from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from .baseScraper import BaseBlogScraper


class MetaEngineeringScraper(BaseBlogScraper):
    def __init__(self):
        super().__init__(
            source_name="Meta Engineering Blog",
            base_url="https://engineering.fb.com/",
            scroll_limit=0  # Using button click
        )
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_soup_pages(self):
        soups = []
        try:
            print(f"🌐 Visiting Meta Engineering Blog — {self.base_url}")
            self.driver.get(self.base_url)

            while True:
                time.sleep(2)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                posts = self.select_posts(soup)
                soups.append(soup)

                # Try to click "Load More"
                try:
                    load_more = self.driver.find_element("css selector", "button.loadmore-btn")
                    if load_more.is_displayed():
                        print("🔄 Clicking 'Load More'...")
                        self.driver.execute_script("arguments[0].click();", load_more)
                        time.sleep(2)
                    else:
                        break
                except Exception:
                    print("✅ No more 'Load More' — finished loading.")
                    break

        finally:
            self.driver.quit()

        return soups

    def select_posts(self, soup):
        return soup.select("article.post")

    def parse_post(self, post):
        a_tag = post.select_one(".entry-title a")
        url = a_tag["href"] if a_tag else None
        title = a_tag.get_text(strip=True) if a_tag else None

        tag_els = post.select("span.cat-links a.category")
        tags = [t.get_text(strip=True) for t in tag_els]

        date_el = post.select_one("time.entry-date.published")
        published_date = None
        if date_el and date_el.get("datetime"):
            published_date = datetime.strptime(date_el["datetime"], "%b %d, %Y").date().isoformat()

        if title and url:
            article = self.enrich_article(title, url, published_date, summary="")
            if tags:
                article["tags"] = tags
            return article

        print(f"⚠️ Missing title or URL for Meta post.")
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

        print(f"✅ Scraped {len(articles)} Meta Engineering posts.")
        return articles
