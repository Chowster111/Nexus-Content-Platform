from datetime import datetime
from typing import List, Optional
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from .baseScraper import BaseBlogScraper
from models.scraper import ScrapedArticle


class SlackScraper(BaseBlogScraper):
    def __init__(self) -> None:
        super().__init__(
            source_name="Slack Engineering Blog",
            base_url="https://slack.engineering/articles/",
            scroll_limit=0
        )
        self.MAX_PAGES: int = 23
        self.PAGE_TEMPLATE: str = "https://slack.engineering/articles/page/{}/"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver: WebDriver = webdriver.Chrome(options=chrome_options)

    def get_soup_pages(self) -> List[BeautifulSoup]:
        """Get BeautifulSoup objects from multiple pages."""
        soups: List[BeautifulSoup] = []
        try:
            for page in range(1, self.MAX_PAGES + 1):
                url: str = self.base_url if page == 1 else self.PAGE_TEMPLATE.format(page)
                print(f"\n🌐 Visiting Slack Engineering page {page}: {url}")
                self.driver.get(url)
                self.driver.implicitly_wait(5)
                soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, "html.parser")
                soups.append(soup)
        finally:
            self.driver.quit()
        return soups

    def select_posts(self, soup: BeautifulSoup) -> List[Tag]:
        """Select post elements from the Slack blog."""
        return soup.select("div.ts-posts-area__main article.ts-entry")

    def parse_post(self, post: Tag) -> Optional[ScrapedArticle]:
        """Parse a single Slack post element."""
        title_el: Optional[Tag] = post.select_one("h2.ts-entry__title a")
        title: Optional[str] = title_el.get_text(strip=True) if title_el else None
        url: Optional[str] = title_el["href"] if title_el else None

        if url and not url.startswith("http"):
            url = f"https://slack.engineering{url}"

        date_el: Optional[Tag] = post.select_one("div.ts-meta-date")
        published_date: Optional[datetime] = None
        if date_el:
            try:
                published_date = datetime.strptime(date_el.get_text(strip=True), "%B %d, %Y")
            except Exception as e:
                print(f"⚠️ Date parse failed: {e}")

        # ✅ Use the excerpt as summary for better keyword extraction
        excerpt_el: Optional[Tag] = post.select_one("p.ts-entry__excerpt")
        summary: str = excerpt_el.get_text(strip=True) if excerpt_el else ""

        # ✅ Extract tags from <article> class attributes, fallback to []
        class_attr: List[str] = post.get("class", [])
        tags: List[str] = [cls.replace("tag-", "") for cls in class_attr if cls.startswith("tag-")]

        if title and url:
            article: Optional[ScrapedArticle] = self.enrich_article(title, url, published_date, summary=summary)

            # ✅ Always pass tags if we found any in HTML
            if article and tags:
                article.tags = tags

            return article

        print(f"⚠️ Missing title or URL, skipping")
        return None

    def scrape(self) -> List[ScrapedArticle]:
        """Main scraping method for Slack articles."""
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

        print(f"✅ Scraped {len(articles)} Slack posts.")
        return articles
