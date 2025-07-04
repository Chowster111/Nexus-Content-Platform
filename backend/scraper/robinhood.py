from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .baseScraper import BaseBlogScraper


class RobinhoodScraper(BaseBlogScraper):
    def __init__(self):
        super().__init__(
            source_name="Robinhood Newsroom",
            base_url="https://newsroom.aboutrobinhood.com/page/1/",
            scroll_limit=0
        )
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

        self.MAX_PAGES = 40

    def get_soup_pages(self):
        soups = []
        try:
            for page in range(1, self.MAX_PAGES + 1):
                url = f"https://newsroom.aboutrobinhood.com/page/{page}/"
                print(f"🌐 Visiting Robinhood Newsroom page {page} — {url}")
                self.driver.get(url)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")

                posts = self.select_posts(soup)
                if not posts:
                    print(f"✅ No posts found on page {page} — stopping.")
                    break

                soups.append(soup)
        finally:
            self.driver.quit()
        return soups

    def select_posts(self, soup):
        return soup.select("div.frontpage-post-box")

    def parse_post(self, post):
        # Title & URL
        title_el = post.select_one("div.frontpage-post-title h2")
        title = title_el.get_text(strip=True) if title_el else None

        link_el = post.select_one("div.frontpage-post-title a")
        url = link_el["href"] if link_el else None

        # Category tag
        cat_el = post.select_one("div.frontpage-post-category span.post-category")
        tags = []
        if cat_el:
            cat_text = cat_el.get_text(strip=True)
            if cat_text:
                tags.append(cat_text)

        # Published date
        date_el = post.select_one("time.entry-date")
        published_date = None
        if date_el and date_el.has_attr("datetime"):
            try:
                published_date = datetime.fromisoformat(date_el["datetime"])
            except Exception as e:
                print(f"⚠️ Date parse failed: {e}")

        # Summary/excerpt
        summary_el = post.select_one("div.frontpage-post-excerpt p")
        summary = summary_el.get_text(strip=True) if summary_el else ""

        if title and url:
            article = self.enrich_article(title, url, published_date, summary)
            if tags:
                article["tags"] = tags
            return article

        print(f"⚠️ Missing title or URL for Robinhood post.")
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

        print(f"✅ Scraped {len(articles)} Robinhood posts.")
        return articles
