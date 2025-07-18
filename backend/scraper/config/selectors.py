"""
CSS selectors and parsing rules for web scrapers.

This module contains CSS selectors and parsing rules used
by different company scrapers.
"""

from typing import Dict, List, Any


class SelectorConfig:
    """Configuration for CSS selectors and parsing rules."""
    
    # Netflix Tech Blog selectors
    NETFLIX = {
        "posts": "div.col.u-xs-size12of12.js-trackPostPresentation",
        "title": "h3 > div",
        "link": "a[href]",
        "date": "time",
        "summary": None
    }
    
    # Airbnb Engineering Blog selectors
    AIRBNB = {
        "posts": "div[data-post-id]",
        "title": "h3 > div",
        "link": "a[href*='airbnb-engineering']",
        "date": "time",
        "summary": None
    }
    
    # Stripe Blog selectors
    STRIPE = {
        "posts": "article.BlogIndexPost",
        "title": ".BlogIndexPost__title a",
        "link": ".BlogIndexPost__title a",
        "date": "time",
        "summary": ".BlogIndexPost__body p"
    }
    
    # Uber Engineering Blog selectors
    UBER = {
        "posts": "article.post",
        "title": "h2.post-title a",
        "link": "h2.post-title a",
        "date": "time.post-date",
        "summary": ".post-excerpt p"
    }
    
    # Tinder Tech Blog selectors
    TINDER = {
        "posts": "div.post",
        "title": "h2.post-title a",
        "link": "h2.post-title a",
        "date": "time.post-date",
        "summary": ".post-excerpt"
    }
    
    # DoorDash Engineering Blog selectors
    DOORDASH = {
        "posts": "article.post",
        "title": "h2.post-title a",
        "link": "h2.post-title a",
        "date": "time.post-date",
        "summary": ".post-excerpt p"
    }
    
    # Meta Engineering Blog selectors
    META = {
        "posts": "div.post",
        "title": "h2.post-title a",
        "link": "h2.post-title a",
        "date": "time.post-date",
        "summary": ".post-excerpt p"
    }
    
    # Notion Engineering Blog selectors
    NOTION = {
        "posts": "article.post",
        "title": "h2.post-title a",
        "link": "h2.post-title a",
        "date": "time.post-date",
        "summary": ".post-excerpt p"
    }
    
    # Robinhood Engineering Blog selectors
    ROBINHOOD = {
        "posts": "div.post",
        "title": "h2.post-title a",
        "link": "h2.post-title a",
        "date": "time.post-date",
        "summary": ".post-excerpt"
    }
    
    # Slack Engineering Blog selectors
    SLACK = {
        "posts": "article.post",
        "title": "h2.post-title a",
        "link": "h2.post-title a",
        "date": "time.post-date",
        "summary": ".post-excerpt p"
    }
    
    @classmethod
    def get_selectors(cls, company: str) -> Dict[str, str]:
        """Get selectors for a specific company."""
        company_upper = company.upper()
        if hasattr(cls, company_upper):
            return getattr(cls, company_upper)
        raise ValueError(f"No selectors found for company: {company}")
    
    @classmethod
    def get_all_companies(cls) -> List[str]:
        """Get list of all supported companies."""
        return [
            "netflix", "airbnb", "stripe", "uber", "tinder",
            "doordash", "meta", "notion", "robinhood", "slack"
        ] 