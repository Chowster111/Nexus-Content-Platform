from fastapi import APIRouter
from http.client import HTTPException

from .utils.trigger_scrape import SCRAPER_MAP, trigger_scrape
from logging_config import logger

router = APIRouter()

@router.post("/select/{source}")
def trigger_scrape_source(source: str):
    source = source.lower()
    logger.info(f"🔍 Scrape request for source: '{source}'")

    instanceFn = SCRAPER_MAP.get(source, None)
    if not instanceFn:
        logger.warning(f"⚠️ Invalid source requested: '{source}'")
        raise HTTPException(status_code=400, detail=f"Invalid source '{source}'. Must be one of {list(SCRAPER_MAP.keys())}")

    try:
        result = trigger_scrape(source, instanceFn().scrape)
        logger.info(f"✅ Scrape completed for source: '{source}'")
        return result
    except Exception as e:
        logger.exception(f"❌ Error scraping source: '{source}'")
        return {"error": str(e)}

@router.post("/all")
def trigger_scrape_all():
    logger.info("📡 Scrape triggered for all sources")
    results = {}

    for source in SCRAPER_MAP:
        try:
            results[source] = trigger_scrape(source, SCRAPER_MAP[source]().scrape)
            logger.info(f"✅ Successfully scraped '{source}'")
        except Exception as e:
            logger.exception(f"❌ Failed scraping '{source}'")
            results[source] = {"error": str(e)}
    
    return results
