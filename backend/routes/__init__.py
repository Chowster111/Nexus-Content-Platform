"""
FastAPI route handlers package.

This package contains all route handlers organized by functionality
and domain, with a unified registry system.
"""

from typing import List, Type
from fastapi import APIRouter

# Import all route controllers
from .auth import AuthController
from .content import ArticlesController, SearchController, RecommendationController
from .interactions import LikesController
from .analytics import AnalyticsController
from .system import HealthController
from .scraping import ScraperController

# Route registry
ROUTE_REGISTRY = {
    "auth": AuthController,
    "articles": ArticlesController,
    "search": SearchController,
    "recommendations": RecommendationController,
    "likes": LikesController,
    "analytics": AnalyticsController,
    "health": HealthController,
    "scraper": ScraperController,
}


def get_all_routers() -> List[APIRouter]:
    """Get all route routers for registration."""
    routers = []
    for controller_class in ROUTE_REGISTRY.values():
        controller = controller_class()
        routers.append(controller)
    return routers


def get_router(name: str) -> APIRouter:
    """Get a specific router by name."""
    if name not in ROUTE_REGISTRY:
        raise ValueError(f"Unknown router: {name}")
    
    controller_class = ROUTE_REGISTRY[name]
    controller = controller_class()
    return controller.router


def get_available_routers() -> List[str]:
    """Get list of all available routers."""
    return list(ROUTE_REGISTRY.keys())


def register_router(name: str, controller_class: Type) -> None:
    """Register a new router controller."""
    ROUTE_REGISTRY[name] = controller_class


__all__ = [
    # Route controllers
    "AuthController",
    "ArticlesController",
    "SearchController",
    "RecommendationController",
    "LikesController",
    "AnalyticsController",
    "HealthController",
    "ScraperController",
    
    # Registry functions
    "get_all_routers",
    "get_router",
    "get_available_routers",
    "register_router",
    
    # Registry
    "ROUTE_REGISTRY"
] 