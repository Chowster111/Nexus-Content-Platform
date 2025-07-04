from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .baseScraper import BaseBlogScraper


class NotionScraper(BaseBlogScraper):
    def __init__(self):
        super().__init__(
            source_name="Notion Blog",
            base_url="https://www.notion.so/blog/page/1",
            scroll_limit=0
        )

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

        self.MAX_PAGES = 10

    def get_soup_pages(self):
        soups = []
        try:
            for page in range(1, self.MAX_PAGES + 1):
                url = f"https://www.notion.so/blog/page/{page}"
                print(f"🌐 Visiting Notion Blog page {page} — {url}")
                self.driver.get(url)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")

                posts = self.select_posts(soup)
                if not posts:
                    print(f"No posts found on page {page} — stopping.")
                    break

                soups.append(soup)
        finally:
            self.driver.quit()
        return soups

    def select_posts(self, soup):
        return soup.select("article.post-preview")

    def parse_post(self, post):
        title_el = post.select_one("h3 a span")
        title = title_el.get_text(strip=True) if title_el else None

        link_el = post.select_one("h3 a")
        url = link_el["href"] if link_el else None
        if url and not url.startswith("http"):
            url = f"https://www.notion.so{url}"

        summary_el = post.select_one("a.postPreview_subtitle__9cBhQ span")
        summary = summary_el.get_text(strip=True) if summary_el else ""

        # Use eyebrow as a category/tag, e.g. 'For Teams'
        eyebrow_el = post.select_one("div.postPreview_eyebrow__uXR9L span")
        tags = []
        if eyebrow_el:
            eyebrow_text = eyebrow_el.get_text(strip=True)
            if eyebrow_text:
                tags.append(eyebrow_text)

        published_date = None  # Notion does not expose published date

        if title and url:
            article = self.enrich_article(title, url, published_date, summary=summary)
            if tags:
                article["tags"] = tags
            return article

        print(f"Missing title or URL for Notion post.")
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
                    print(f"Error scraping post: {e}")

        print(f"Scraped {len(articles)} Notion posts.")
        return articles
