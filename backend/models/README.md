# Models Directory

This directory contains all Pydantic models used throughout the backend, organized by domain for clarity and maintainability.

## Structure

Each file contains models for a specific domain or feature:

- `article.py`         — Article, ArticleResponse, ArticleCategory, ArticleSource
- `user.py`            — User
- `auth.py`            — SignupRequest, SigninRequest, AuthResponse
- `analytics.py`       — TagCount
- `recommendation.py`  — RecommendationRequest, RecommendationResponse
- `scraper.py`         — ScraperConfig, ScrapedArticle, ScraperResult
- `likes.py`           — LikeRequest, LikeResponse, LikeRecord
- `search.py`          — SearchResult, SearchResponse, SearchRequest
- `health.py`          — HealthCheckResponse, SystemStatus, DetailedHealthResponse
- `models.py`          — Re-exports all models for backward compatibility
- `__init__.py`        — Re-exports all models for convenient imports

## Import Patterns

### Preferred (Explicit) Imports

For new code, **import models directly from their submodules** for clarity and IDE support:

```python
from models.article import Article, ArticleResponse
from models.auth import SignupRequest, AuthResponse
from models.scraper import ScrapedArticle
```

### Backward-Compatible Imports

For legacy code or convenience, you can still import from the top-level `models` package:

```python
from models import Article, ArticleResponse, SignupRequest, ScrapedArticle
```

This works because `models/models.py` and `models/__init__.py` re-export all models.

## Adding New Models

- Place new models in the most appropriate submodule (or create a new one if needed)
- Add a docstring to each model explaining its purpose and validation
- Update `models/models.py` and `models/__init__.py` to re-export the new model if you want it available at the top level

## Why Modularize?

- **Easier navigation:** Quickly find and update models by domain
- **Fewer merge conflicts:** Smaller files, less overlap
- **Better code clarity:** Imports show exactly which models are used
- **Scalability:** Add new features without cluttering a single file

## Example Usage

```python
# In a route or service
from models.article import ArticleResponse

# Validate data from the database
try:
    article = ArticleResponse(**db_row)
except ValidationError as ve:
    logger.error(f"Validation error: {ve}")
```

---