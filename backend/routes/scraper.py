# routes/scraper_controller.py

from fastapi import APIRouter, HTTPException
from logging_config import logger
from .utils.retry import with_backoff
from .utils.trigger_scrape import SCRAPER_MAP, trigger_scrape

class ScraperController:
    def __init__(self):
        self.router = APIRouter()
        self.router.post("/select/{source}")(self.trigger_scrape_source)
        self.router.post("/all")(self.trigger_scrape_all)

    @with_backoff()
    def run_scrape(self, source: str, scrape_fn):
        return trigger_scrape(source, scrape_fn)

    def trigger_scrape_source(self, source: str):
        source = source.lower()
        logger.info(f"🔍 Scrape request for source: '{source}'")

        instance_fn = SCRAPER_MAP.get(source)
        if not instance_fn:
            logger.warning(f"⚠️ Invalid source requested: '{source}'")
            raise HTTPException(status_code=400, detail=f"Invalid source '{source}'. Must be one of {list(SCRAPER_MAP.keys())}")

        try:
            result = self.run_scrape(source, instance_fn().scrape)
            logger.info(f"✅ Scrape completed for source: '{source}'")
            return result
        except Exception as e:
            logger.exception(f"❌ Error scraping source: '{source}'")
            return {"error": str(e)}

    def trigger_scrape_all(self):
        logger.info("📡 Scrape triggered for all sources")
        results = {}

        for source in SCRAPER_MAP:
            try:
                results[source] = self.run_scrape(source, SCRAPER_MAP[source]().scrape)
                logger.info(f"✅ Successfully scraped '{source}'")
            except Exception as e:
                logger.exception(f"❌ Failed scraping '{source}'")
                results[source] = {"error": str(e)}
        
        return results
