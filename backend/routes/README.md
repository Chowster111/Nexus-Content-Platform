# Routes Directory Structure

This directory contains FastAPI route handlers organized by functionality and domain.

## Directory Structure

```
routes/
├── __init__.py                 # Main exports and route registry
├── auth/                       # Authentication and user management routes
│   ├── __init__.py
│   ├── auth.py                # User authentication (signup/signin)
│   └── users.py               # User profile and management
├── content/                    # Content-related routes
│   ├── __init__.py
│   ├── articles.py            # Article CRUD and filtering
│   ├── search.py              # Semantic search functionality
│   └── recommendations.py     # Recommendation system
├── interactions/               # User interaction routes
│   ├── __init__.py
│   ├── likes.py               # User likes/dislikes
│   └── feedback.py            # User feedback and ratings
├── analytics/                  # Analytics and reporting routes
│   ├── __init__.py
│   ├── metrics.py             # Analytics metrics
│   ├── reports.py             # Report generation
│   └── insights.py            # Data insights and trends
├── system/                     # System and infrastructure routes
│   ├── __init__.py
│   ├── health.py              # Health checks and monitoring
│   └── admin.py               # Administrative functions
├── scraping/                   # Content scraping routes
│   ├── __init__.py
│   ├── scraper.py             # Web scraping endpoints
│   └── triggers.py            # Scraping triggers and scheduling
└── utils/                      # Shared utilities
    ├── __init__.py
    ├── retry.py               # Retry decorators
    ├── embedding_utils.py     # Embedding utilities
    └── trigger_scrape.py      # Scraping trigger utilities
```

## Route Categories

### Authentication (`auth/`)
- **auth.py**: User registration, login, and authentication
- **users.py**: User profile management and user-related operations

### Content (`content/`)
- **articles.py**: Article retrieval, filtering, and CRUD operations
- **search.py**: Semantic search and content discovery
- **recommendations.py**: Personalized content recommendations

### Interactions (`interactions/`)
- **likes.py**: User likes/dislikes for articles
- **feedback.py**: User feedback, ratings, and comments

### Analytics (`analytics/`)
- **metrics.py**: Analytics metrics and data collection
- **reports.py**: Report generation and data aggregation
- **insights.py**: Data insights and trend analysis

### System (`system/`)
- **health.py**: Health checks, monitoring, and system status
- **admin.py**: Administrative functions and system management

### Scraping (`scraping/`)
- **scraper.py**: Web scraping endpoints and controls
- **triggers.py**: Scraping triggers and scheduling

## Usage

### Importing Routes
```python
from routes.auth.auth import AuthController
from routes.content.articles import ArticlesController
from routes.analytics.metrics import AnalyticsController
```

### Registering Routes
```python
from fastapi import FastAPI
from routes import get_all_routers

app = FastAPI()

# Register all routes
routers = get_all_routers()
for router in routers:
    app.include_router(router.router, prefix="/api")
```

## Adding New Routes

1. **Identify the category**: Choose the appropriate subdirectory
2. **Create controller class**: Inherit from base controller if needed
3. **Implement routes**: Use FastAPI decorators and proper validation
4. **Add to registry**: Update the relevant `__init__.py` files
5. **Add documentation**: Include comprehensive docstrings and examples

## Route Patterns

### Controller Structure
```python
class ExampleController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.register_routes()
    
    def register_routes(self) -> None:
        # Route definitions here
        pass
```

### Error Handling
- Use proper HTTP status codes
- Include detailed error messages
- Log errors for debugging
- Validate input data

### Documentation
- Include comprehensive docstrings
- Provide example requests/responses
- Document error scenarios
- Use proper FastAPI tags 