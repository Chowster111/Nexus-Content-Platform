from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .baseScraper import BaseBlogScraper


class SlackScraper(BaseBlogScraper):
    def __init__(self):
        super().__init__(
            source_name="Slack Engineering Blog",
            base_url="https://slack.engineering/articles/",
            scroll_limit=0
        )
        self.MAX_PAGES = 23
        self.PAGE_TEMPLATE = "https://slack.engineering/articles/page/{}/"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_soup_pages(self):
        soups = []
        try:
            for page in range(1, self.MAX_PAGES + 1):
                url = self.base_url if page == 1 else self.PAGE_TEMPLATE.format(page)
                print(f"\n🌐 Visiting Slack Engineering page {page}: {url}")
                self.driver.get(url)
                self.driver.implicitly_wait(5)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                soups.append(soup)
        finally:
            self.driver.quit()
        return soups

    def select_posts(self, soup):
        return soup.select("div.ts-posts-area__main article.ts-entry")

    def parse_post(self, post):
        title_el = post.select_one("h2.ts-entry__title a")
        title = title_el.get_text(strip=True) if title_el else None
        url = title_el["href"] if title_el else None

        if url and not url.startswith("http"):
            url = f"https://slack.engineering{url}"

        date_el = post.select_one("div.ts-meta-date")
        published_date = None
        if date_el:
            try:
                published_date = datetime.strptime(date_el.get_text(strip=True), "%B %d, %Y")
            except Exception as e:
                print(f"⚠️ Date parse failed: {e}")

        # ✅ Use the excerpt as summary for better keyword extraction
        excerpt_el = post.select_one("p.ts-entry__excerpt")
        summary = excerpt_el.get_text(strip=True) if excerpt_el else ""

        # ✅ Extract tags from <article> class attributes, fallback to []
        class_attr = post.get("class", [])
        tags = [cls.replace("tag-", "") for cls in class_attr if cls.startswith("tag-")]

        if title and url:
            article = self.enrich_article(title, url, published_date, summary=summary)

            # ✅ Always pass tags if we found any in HTML
            if tags:
                article["tags"] = tags

            return article

        print(f"⚠️ Missing title or URL, skipping")
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

        print(f"✅ Scraped {len(articles)} Slack posts.")
        return articles
