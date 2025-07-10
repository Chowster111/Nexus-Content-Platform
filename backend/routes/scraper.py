# routes/scraper_controller.py

from typing import Dict, Any, List, Callable, Optional
from fastapi import APIRouter, HTTPException
from logging_config import logger
from .utils.retry import with_backoff
from .utils.trigger_scrape import SCRAPER_MAP, trigger_scrape
from ..models.scraper import ScraperResult, ScrapedArticle
from pydantic import ValidationError


class ScraperController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.post("/select/{source}")(self.trigger_scrape_source)
        self.router.post("/all")(self.trigger_scrape_all)

    @with_backoff()
    def run_scrape(self, source: str, scrape_fn: Callable[[], List[ScrapedArticle]]) -> ScraperResult:
        """Run scraping for a specific source."""
        return trigger_scrape(source, scrape_fn)

    def trigger_scrape_source(self, source: str) -> ScraperResult:
        """Trigger scraping for a specific source."""
        source = source.lower()
        logger.info(f"Scrape request for source: '{source}'")

        instance_fn: Optional[Callable] = SCRAPER_MAP.get(source)
        if not instance_fn:
            logger.warning(f"ERROR Invalid source requested: '{source}'")
            raise HTTPException(status_code=400, detail=f"Invalid source '{source}'. Must be one of {list(SCRAPER_MAP.keys())}")

        try:
            result: ScraperResult = self.run_scrape(source, instance_fn().scrape)
            # Validate articles in result
            valid_articles = []
            errors = []
            for article in result.articles:
                try:
                    valid_articles.append(ScrapedArticle(**article.dict()))
                except ValidationError as ve:
                    logger.error(f"Validation error for scraped article: {article} | {ve}")
                    errors.append({"article": article, "error": str(ve)})
            if errors:
                logger.warning(f"Some scraped articles could not be validated: {errors}")
            result.articles = valid_articles
            return result
        except Exception as e:
            logger.exception(f"ERROR scraping source: '{source}'")
            return ScraperResult(source=source, success=False, error=str(e), articles=[])

    def trigger_scrape_all(self) -> Dict[str, ScraperResult]:
        """Trigger scraping for all sources."""
        logger.info("Scrape triggered for all sources")
        results: Dict[str, ScraperResult] = {}

        for source in SCRAPER_MAP:
            try:
                result = self.run_scrape(source, SCRAPER_MAP[source]().scrape)
                # Validate articles in result
                valid_articles = []
                errors = []
                for article in result.articles:
                    try:
                        valid_articles.append(ScrapedArticle(**article.dict()))
                    except ValidationError as ve:
                        logger.error(f"Validation error for scraped article: {article} | {ve}")
                        errors.append({"article": article, "error": str(ve)})
                if errors:
                    logger.warning(f"Some scraped articles for {source} could not be validated: {errors}")
                result.articles = valid_articles
                results[source] = result
                logger.info(f"SUCCESS: Successfully scraped '{source}'")
            except Exception as e:
                logger.exception(f"ERROR Failed scraping '{source}'")
                results[source] = ScraperResult(source=source, success=False, error=str(e), articles=[])
        return results
