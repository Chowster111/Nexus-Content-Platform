# Models Directory Structure

> **Note:**
> Both `__init__.py` and `models.py` in this directory currently serve the same purpose: they re-export all models for backward compatibility. This allows both old and new import styles to work. Once all code is migrated to use the new import paths (directly from submodules or via `__init__.py`), `models.py` can be safely removed.

This directory contains all Pydantic models organized by domain and functionality.

## Directory Structure

```
models/
├── __init__.py                 # Main exports and backward compatibility
├── core/                       # Core domain models
│   ├── __init__.py
│   ├── article.py             # Article models and enums
│   ├── user.py                # User models
│   └── base.py                # Base models and common types
├── api/                        # API request/response models
│   ├── __init__.py
│   ├── auth.py                # Authentication models
│   ├── search.py              # Search request/response models
│   ├── recommendation.py      # Recommendation models
│   └── likes.py               # User interaction models
├── analytics/                  # Analytics and reporting models
│   ├── __init__.py
│   ├── metrics.py             # Analytics metrics models
│   └── reports.py             # Report generation models
├── system/                     # System and infrastructure models
│   ├── __init__.py
│   ├── health.py              # Health check models
│   └── monitoring.py          # Monitoring and logging models
├── scraping/                   # Content scraping models
│   ├── __init__.py
│   ├── scraper.py             # Scraper configuration and results
│   └── content.py             # Content processing models
└── events/                     # Event-driven architecture models
    ├── __init__.py
    ├── base.py                # Base event models
    ├── article_events.py      # Article-related events
    ├── user_events.py         # User interaction events
    └── system_events.py       # System and monitoring events
```

## Model Categories

### Core Models (`core/`)
- **article.py**: Article entities, categories, sources
- **user.py**: User entities and profiles
- **base.py**: Base classes and common types

### API Models (`api/`)
- **auth.py**: Authentication requests/responses
- **search.py**: Search functionality models
- **recommendation.py**: Recommendation system models
- **likes.py**: User interaction models

### Analytics Models (`analytics/`)
- **metrics.py**: Analytics metrics and aggregations
- **reports.py**: Report generation and data structures

### System Models (`system/`)
- **health.py**: Health check and monitoring
- **monitoring.py**: System monitoring and observability

### Scraping Models (`scraping/`)
- **scraper.py**: Web scraper configuration
- **content.py**: Content processing and validation

### Event Models (`events/`)
- **base.py**: Base event classes
- **article_events.py**: Article processing events
- **user_events.py**: User interaction events
- **system_events.py**: System and monitoring events

## Import Guidelines

### For New Code
Import models directly from their specific modules:
```python
from models.core.article import Article, ArticleResponse
from models.api.auth import SignupRequest, AuthResponse
from models.analytics.metrics import TagCount
```

### For Backward Compatibility
The main `__init__.py` re-exports commonly used models:
```python
from models import Article, ArticleResponse, SignupRequest
```

## Adding New Models

1. **Identify the domain**: Choose the appropriate subdirectory
2. **Follow naming conventions**: Use descriptive names and proper validation
3. **Add to exports**: Update the relevant `__init__.py` files
4. **Update main exports**: Add to `models/__init__.py` if commonly used

## Validation Guidelines

- Use Pydantic validators for complex validation logic
- Include field descriptions for API documentation
- Add proper error messages for validation failures
- Use enums for constrained values
- Include proper type hints for all fields