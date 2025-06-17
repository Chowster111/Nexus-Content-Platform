# uber_scraper.py
from datetime import datetime
from bs4 import BeautifulSoup
from .baseScraper import BaseBlogScraper

device = "cpu"
class UberScraper(BaseBlogScraper):
    def __init__(self):
        super().__init__(
            source_name="Uber Engineering Blog",
            base_url="https://www.uber.com/en-CA/blog/engineering/page/1",
            scroll_limit=0  # no scroll needed, we paginate
        )
        self.MAX_PAGES = 20
        self.PAGE_TEMPLATE = "https://www.uber.com/en-CA/blog/engineering/page/{}"

    def get_soup_pages(self):
        soups = []
        for page in range(1, self.MAX_PAGES + 1):
            print(f"\n🌐 Visiting Uber page {page}")
            self.driver.get(self.PAGE_TEMPLATE.format(page))
            self.driver.implicitly_wait(5)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            post_blocks = soup.select("div[data-baseweb='flex-grid-item']")
            if not post_blocks:
                print("❌ No more posts found. Stopping.")
                break
            soups.append(soup)
        self.driver.quit()
        return soups

    def select_posts(self, soup):
        return soup.select("div[data-baseweb='flex-grid-item']")

    def parse_post(self, post):
        title_el = post.select_one("h2")
        link_el = post.select_one("a[href]")
        date_el = post.select_one("p")

        title = title_el.get_text(strip=True) if title_el else None
        url = link_el["href"].split("?")[0] if link_el else None

        date_text = date_el.get_text(strip=True).split(" / ")[0] if date_el else None
        published_date = None
        if date_text:
            try:
                published_date = datetime.strptime(date_text, "%B %d, %Y")
            except Exception as e:
                print(f"⚠️ Date parse failed: {date_text} — {e}")

        if title and url:
            return self.enrich_article(title, url, published_date, summary="")

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
