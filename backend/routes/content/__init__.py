"""
Content-related routes.

This module contains routes for articles, search, and recommendations.
"""

from .articles import ArticlesController
from .search import SearchController
from .recommendations import RecommendationController

__all__ = [
    "ArticlesController",
    "SearchController",
    "RecommendationController"
] 