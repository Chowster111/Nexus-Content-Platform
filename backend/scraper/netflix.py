from datetime import datetime

from .baseScraper import BaseBlogScraper

device = "cpu"
class NetflixScraper(BaseBlogScraper):
    def __init__(self):
        super().__init__("Netflix Tech Blog", "https://netflixtechblog.com", scroll_limit=50)

    def select_posts(self, soup):
        return soup.select("div.col.u-xs-size12of12.js-trackPostPresentation")

    def parse_post(self, post):
        title_el = post.select_one("h3 > div")
        link_el = post.select_one("a[href]")
        time_el = post.select_one("time")

        title = title_el.get_text(strip=True) if title_el else None
        url = link_el["href"] if link_el else None
        published_date = (
            datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
            if time_el else None
        )

        if title and url:
            return self.enrich_article(title, url, published_date)
        return None
