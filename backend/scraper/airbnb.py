from datetime import datetime

from .baseScraper import BaseBlogScraper

device = "cpu"
class AirbnbScraper(BaseBlogScraper):
    def __init__(self):
        super().__init__("Airbnb Engineering Blog", "https://medium.com/airbnb-engineering")

    def select_posts(self, soup):
        return soup.select("div[data-post-id]")

    def parse_post(self, post):
        title_el = post.select_one("h3 > div")
        link_el = post.select_one("a[href*='airbnb-engineering']")
        time_el = post.select_one("time")

        title = title_el.get_text(strip=True) if title_el else None
        url = link_el["href"].split("?")[0] if link_el else None
        published_date = (
            datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
            if time_el and "datetime" in time_el.attrs else None
        )

        if title and url:
            return self.enrich_article(title, url, published_date)
        return None
