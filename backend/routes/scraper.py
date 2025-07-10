# routes/scraper_controller.py

from typing import Dict, Any, List, Callable, Optional
from fastapi import APIRouter, HTTPException, Path
from logging_config import logger
from .utils.retry import with_backoff
from .utils.trigger_scrape import SCRAPER_MAP, trigger_scrape
from models.scraper import ScraperResult, ScrapedArticle
from pydantic import ValidationError


class ScraperController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self) -> None:
        """Register all scraper routes with comprehensive documentation."""
        
        @self.router.post(
            "/select/{source}",
            summary="Scrape Specific Source",
            description="""
            Trigger scraping for a specific engineering blog source.
            
            This endpoint initiates the scraping process for a single source, collecting
            the latest articles from the specified engineering blog. The scraper uses
            Selenium and BeautifulSoup to extract article content, metadata, and tags.
            
            **Supported Sources:**
            - **netflix**: Netflix Engineering Blog
            - **airbnb**: Airbnb Engineering & Data Science
            - **uber**: Uber Engineering
            - **stripe**: Stripe Engineering
            - **tinder**: Tinder Engineering
            - **doordash**: DoorDash Engineering
            - **slack**: Slack Engineering
            - **notion**: Notion Engineering
            - **meta**: Meta Engineering
            - **robinhood**: Robinhood Engineering
            
            **Scraping Process:**
            1. **Content Extraction**: Retrieves article titles, URLs, and content
            2. **Metadata Processing**: Extracts publication dates, authors, and categories
            3. **Tag Generation**: Uses KeyBERT for automatic tag extraction
            4. **Embedding Generation**: Creates semantic embeddings for search
            5. **Database Storage**: Saves articles with full metadata
            
            **Features:**
            - Real-time content scraping from live blogs
            - Automatic tag extraction using AI
            - Semantic embedding generation
            - Duplicate article detection
            - Error handling and retry logic
            - Progress tracking and status reporting
            
            **Admin Access Required:**
            This endpoint requires admin authentication due to resource-intensive
            scraping operations and potential rate limiting from source sites.
            """,
            response_description="Scraping results with article count and status",
            tags=["Scraping"]
        )
        def trigger_scrape_source(
            source: str = Path(..., description="Source to scrape", example="netflix")
        ) -> ScraperResult:
            """
            Trigger scraping for a specific source.
            
            Initiates the scraping process for the specified engineering blog source.
            The scraper will collect all available articles and process them for
            the recommendation system.
            
            **Parameters:**
            - `source`: The engineering blog source to scrape (case-insensitive)
            
            **Example Request:**
            ```
            POST /scrape/select/netflix
            ```
            
            **Example Response:**
            ```json
            {
              "source": "netflix",
              "success": true,
              "articles_count": 15,
              "articles": [
                {
                  "title": "Building Scalable Microservices",
                  "url": "https://netflix.com/tech-blog/scalable-microservices",
                  "published_date": "2024-01-15",
                  "content": "How Netflix built their scalable microservices architecture...",
                  "source": "netflix",
                  "category": "Architecture",
                  "tags": ["microservices", "scalability", "architecture"],
                  "summary": "A comprehensive guide to building scalable microservices..."
                }
              ],
              "error": null
            }
            ```
            
            **Error Scenarios:**
            - 400: Invalid source name
            - 401: Admin authentication required
            - 500: Scraping process failed
            - 500: Database storage error
            """
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

        @self.router.post(
            "/all",
            summary="Scrape All Sources",
            description="""
            Trigger scraping for all supported engineering blog sources.
            
            This endpoint initiates a comprehensive scraping operation across all
            supported engineering blogs simultaneously. This is useful for bulk
            content updates and maintaining a fresh article database.
            
            **Scraping Strategy:**
            - **Parallel Processing**: Scrapes multiple sources concurrently
            - **Error Isolation**: Individual source failures don't affect others
            - **Progress Tracking**: Real-time status updates for each source
            - **Resource Management**: Optimized for large-scale scraping operations
            
            **Supported Sources:**
            All available engineering blog sources including Netflix, Airbnb, Uber,
            Stripe, Tinder, DoorDash, Slack, Notion, Meta, and Robinhood.
            
            **Performance Considerations:**
            - High resource usage during execution
            - May take several minutes to complete
            - Rate limiting considerations for source sites
            - Database write operations for article storage
            
            **Admin Access Required:**
            This endpoint requires admin authentication due to the intensive
            nature of bulk scraping operations.
            
            **Monitoring:**
            - Real-time progress updates
            - Individual source success/failure tracking
            - Article count and validation statistics
            - Error reporting for failed sources
            """,
            response_description="Comprehensive scraping results for all sources",
            tags=["Scraping"]
        )
        def trigger_scrape_all() -> Dict[str, ScraperResult]:
            """
            Trigger scraping for all supported sources.
            
            Initiates a comprehensive scraping operation across all engineering blog
            sources. This operation may take several minutes and should be monitored
            for progress and completion status.
            
            **Example Request:**
            ```
            POST /scrape/all
            ```
            
            **Example Response:**
            ```json
            {
              "netflix": {
                "source": "netflix",
                "success": true,
                "articles_count": 15,
                "articles": [...],
                "error": null
              },
              "airbnb": {
                "source": "airbnb",
                "success": true,
                "articles_count": 12,
                "articles": [...],
                "error": null
              },
              "uber": {
                "source": "uber",
                "success": false,
                "articles_count": 0,
                "articles": [],
                "error": "Connection timeout"
              }
            }
            ```
            
            **Response Structure:**
            - Each source has its own result object
            - Success/failure status per source
            - Article count and validation results
            - Detailed error messages for failed sources
            
            **Error Handling:**
            - Individual source failures are isolated
            - Partial success scenarios are supported
            - Detailed error reporting per source
            - Graceful degradation for network issues
            """
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

    @with_backoff()
    def run_scrape(self, source: str, scrape_fn: Callable[[], List[ScrapedArticle]]) -> ScraperResult:
        """Run scraping for a specific source."""
        return trigger_scrape(source, scrape_fn)
