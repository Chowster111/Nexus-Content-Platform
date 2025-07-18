"""
Scraper settings and configuration.

This module contains default settings and configuration options
for all web scrapers in the system.
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class ScraperSettings:
    """Default settings for web scrapers."""
    
    # Default scroll limits
    DEFAULT_SCROLL_LIMIT: int = 30
    MAX_SCROLL_LIMIT: int = 100
    
    # Default timeouts
    PAGE_LOAD_TIMEOUT: int = 30
    SCROLL_DELAY: float = 2.0
    
    # Default retry settings
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0
    
    # Default user agent
    DEFAULT_USER_AGENT: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    
    # Chrome options
    CHROME_OPTIONS: Dict[str, Any] = {
        "--no-sandbox": True,
        "--disable-dev-shm-usage": True,
        "--disable-gpu": True,
        "--disable-extensions": True,
        "--disable-plugins": True,
        "--disable-images": True,
        "--disable-javascript": False,
    }
    
    # Rate limiting
    RATE_LIMIT_DELAY: float = 1.0
    MAX_REQUESTS_PER_MINUTE: int = 60


# Global settings instance
SCRAPER_SETTINGS = ScraperSettings()


def get_scraper_settings() -> ScraperSettings:
    """Get the global scraper settings."""
    return SCRAPER_SETTINGS


def update_scraper_settings(**kwargs) -> None:
    """Update scraper settings with new values."""
    for key, value in kwargs.items():
        if hasattr(SCRAPER_SETTINGS, key):
            setattr(SCRAPER_SETTINGS, key, value) 