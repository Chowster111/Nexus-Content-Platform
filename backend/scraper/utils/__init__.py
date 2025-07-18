"""
Shared utilities for web scrapers.

This module contains common utilities, helpers, and constants
used across different web scrapers.
"""

from .embedding_utils import (
    category_embeddings,
    classify_article_semantically,
    kw_model,
    safe_encode,
    semantic_model
)
from .constants import CATEGORIES
from .helpers import (
    safe_get_text,
    safe_get_attribute,
    parse_date,
    clean_url,
    extract_summary,
    wait_for_page_load,
    scroll_page_smoothly,
    validate_article_data,
    log_scraping_progress
)

__all__ = [
    # Embedding utilities
    "category_embeddings",
    "classify_article_semantically",
    "kw_model",
    "safe_encode",
    "semantic_model",
    
    # Constants
    "CATEGORIES",
    
    # Helper functions
    "safe_get_text",
    "safe_get_attribute",
    "parse_date",
    "clean_url",
    "extract_summary",
    "wait_for_page_load",
    "scroll_page_smoothly",
    "validate_article_data",
    "log_scraping_progress"
] 