"""
Helper functions for web scrapers.

This module contains common utility functions used across
different web scrapers.
"""

import time
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup, Tag
from selenium.webdriver.remote.webdriver import WebDriver


logger = logging.getLogger(__name__)


def safe_get_text(element: Optional[Tag], strip: bool = True) -> Optional[str]:
    """Safely extract text from a BeautifulSoup element."""
    if element is None:
        return None
    try:
        text = element.get_text(strip=strip)
        return text if text else None
    except Exception as e:
        logger.warning(f"Error extracting text from element: {e}")
        return None


def safe_get_attribute(element: Optional[Tag], attribute: str) -> Optional[str]:
    """Safely get an attribute from a BeautifulSoup element."""
    if element is None:
        return None
    try:
        return element.get(attribute)
    except Exception as e:
        logger.warning(f"Error getting attribute {attribute} from element: {e}")
        return None


def parse_date(date_string: Optional[str], formats: List[str] = None) -> Optional[datetime]:
    """Parse date string with multiple format support."""
    if not date_string:
        return None
    
    if formats is None:
        formats = [
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%B %d, %Y",
            "%b %d, %Y"
        ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    logger.warning(f"Could not parse date: {date_string}")
    return None


def clean_url(url: Optional[str]) -> Optional[str]:
    """Clean and normalize URL."""
    if not url:
        return None
    
    # Remove query parameters
    url = url.split('?')[0]
    
    # Ensure proper protocol
    if url.startswith('//'):
        url = 'https:' + url
    elif url.startswith('/'):
        # This would need base URL context
        pass
    
    return url.strip()


def extract_summary(element: Optional[Tag], max_length: int = 200) -> str:
    """Extract and clean summary text from an element."""
    if element is None:
        return ""
    
    text = safe_get_text(element, strip=True)
    if not text:
        return ""
    
    # Clean and truncate
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())
    
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text


def wait_for_page_load(driver: WebDriver, timeout: int = 30) -> bool:
    """Wait for page to load completely."""
    try:
        # Wait for document ready state
        driver.execute_script("return document.readyState") == "complete"
        time.sleep(2)  # Additional buffer
        return True
    except Exception as e:
        logger.warning(f"Error waiting for page load: {e}")
        return False


def scroll_page_smoothly(driver: WebDriver, scroll_limit: int = 30, delay: float = 2.0) -> None:
    """Scroll page smoothly to load dynamic content."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    for i in range(scroll_limit):
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
        
        # Check if page height changed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
        logger.debug(f"Scrolled {i+1}/{scroll_limit} times")


def validate_article_data(title: str, url: str) -> bool:
    """Validate basic article data."""
    if not title or not title.strip():
        return False
    
    if not url or not url.strip():
        return False
    
    # Basic URL validation
    if not (url.startswith('http://') or url.startswith('https://')):
        return False
    
    return True


def log_scraping_progress(current: int, total: int, company: str) -> None:
    """Log scraping progress."""
    progress = (current / total) * 100 if total > 0 else 0
    logger.info(f"Scraping {company}: {current}/{total} articles ({progress:.1f}%)") 