"""
Scraper configuration and settings.

This module contains configuration settings, defaults, and
CSS selectors for web scrapers.
"""

from .settings import ScraperSettings
from .selectors import SelectorConfig

__all__ = [
    "ScraperSettings",
    "SelectorConfig"
] 