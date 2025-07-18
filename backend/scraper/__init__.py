"""
Web scraper package for engineering blogs.

This package contains scrapers for various engineering blogs,
organized by company with a unified registry system.
"""

from typing import Dict, Type, List
from .base import BaseBlogScraper
from .companies import (
    NetflixScraper, AirbnbScraper, StripeScraper, UberScraper,
    TinderScraper, DoorDashScraper, MetaScraper, NotionScraper,
    RobinhoodScraper, SlackScraper
)
from .config import ScraperSettings, SelectorConfig
from .utils import (
    safe_get_text, safe_get_attribute, parse_date, clean_url,
    extract_summary, validate_article_data, log_scraping_progress
)

# Scraper registry
SCRAPER_REGISTRY: Dict[str, Type[BaseBlogScraper]] = {
    "netflix": NetflixScraper,
    "airbnb": AirbnbScraper,
    "stripe": StripeScraper,
    "uber": UberScraper,
    "tinder": TinderScraper,
    "doordash": DoorDashScraper,
    "meta": MetaScraper,
    "notion": NotionScraper,
    "robinhood": RobinhoodScraper,
    "slack": SlackScraper
}


def get_scraper(company: str) -> BaseBlogScraper:
    """Get a scraper instance for the specified company."""
    if company.lower() not in SCRAPER_REGISTRY:
        raise ValueError(f"Unknown company: {company}")
    
    scraper_class = SCRAPER_REGISTRY[company.lower()]
    return scraper_class()


def get_available_companies() -> List[str]:
    """Get list of all available companies."""
    return list(SCRAPER_REGISTRY.keys())


def get_scraper_class(company: str) -> Type[BaseBlogScraper]:
    """Get the scraper class for the specified company."""
    if company.lower() not in SCRAPER_REGISTRY:
        raise ValueError(f"Unknown company: {company}")
    
    return SCRAPER_REGISTRY[company.lower()]


def register_scraper(company: str, scraper_class: Type[BaseBlogScraper]) -> None:
    """Register a new scraper class."""
    SCRAPER_REGISTRY[company.lower()] = scraper_class


__all__ = [
    # Base classes
    "BaseBlogScraper",
    
    # Company scrapers
    "NetflixScraper",
    "AirbnbScraper", 
    "StripeScraper",
    "UberScraper",
    "TinderScraper",
    "DoorDashScraper",
    "MetaScraper",
    "NotionScraper",
    "RobinhoodScraper",
    "SlackScraper",
    
    # Configuration
    "ScraperSettings",
    "SelectorConfig",
    
    # Utilities
    "safe_get_text",
    "safe_get_attribute", 
    "parse_date",
    "clean_url",
    "extract_summary",
    "validate_article_data",
    "log_scraping_progress",
    
    # Registry functions
    "get_scraper",
    "get_available_companies",
    "get_scraper_class",
    "register_scraper"
] 