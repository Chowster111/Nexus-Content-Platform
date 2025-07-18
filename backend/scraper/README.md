# Scraper Directory Structure

This directory contains web scrapers for engineering blogs, organized by company and functionality.

## Directory Structure

```
scraper/
├── __init__.py                 # Main exports and scraper registry
├── base/                       # Base classes and common functionality
│   ├── __init__.py
│   ├── base_scraper.py        # Base scraper class
│   └── common.py              # Common utilities and helpers
├── companies/                  # Company-specific scrapers
│   ├── __init__.py
│   ├── netflix.py             # Netflix Tech Blog scraper
│   ├── airbnb.py              # Airbnb Engineering Blog scraper
│   ├── stripe.py              # Stripe Blog scraper
│   ├── uber.py                # Uber Engineering Blog scraper
│   ├── tinder.py              # Tinder Tech Blog scraper
│   ├── doordash.py            # DoorDash Engineering Blog scraper
│   ├── meta.py                # Meta Engineering Blog scraper
│   ├── notion.py              # Notion Engineering Blog scraper
│   ├── robinhood.py           # Robinhood Engineering Blog scraper
│   └── slack.py               # Slack Engineering Blog scraper
├── utils/                      # Shared utilities
│   ├── __init__.py
│   ├── embedding_utils.py     # Embedding and semantic analysis
│   ├── constants.py           # Constants and configurations
│   └── helpers.py             # Helper functions
├── config/                     # Configuration and settings
│   ├── __init__.py
│   ├── settings.py            # Scraper settings and defaults
│   └── selectors.py           # CSS selectors and parsing rules
└── Dockerfile                  # Container configuration
```

## Scraper Categories

### Base Classes (`base/`)
- **base_scraper.py**: Abstract base class for all scrapers
- **common.py**: Common utilities and helper functions

### Company Scrapers (`companies/`)
- **netflix.py**: Netflix Tech Blog
- **airbnb.py**: Airbnb Engineering Blog
- **stripe.py**: Stripe Blog
- **uber.py**: Uber Engineering Blog
- **tinder.py**: Tinder Tech Blog
- **doordash.py**: DoorDash Engineering Blog
- **meta.py**: Meta Engineering Blog
- **notion.py**: Notion Engineering Blog
- **robinhood.py**: Robinhood Engineering Blog
- **slack.py**: Slack Engineering Blog

### Utilities (`utils/`)
- **embedding_utils.py**: Semantic analysis and embeddings
- **constants.py**: Categories and configuration constants
- **helpers.py**: Helper functions for scraping

### Configuration (`config/`)
- **settings.py**: Scraper settings and defaults
- **selectors.py**: CSS selectors and parsing rules

## Usage

### Importing Scrapers
```python
from scraper.companies.netflix import NetflixScraper
from scraper.companies.stripe import StripeScraper
from scraper.base.base_scraper import BaseBlogScraper
```

### Running Scrapers
```python
# Individual scraper
netflix_scraper = NetflixScraper()
articles = netflix_scraper.scrape()

# Using scraper registry
from scraper import get_scraper
scraper = get_scraper("netflix")
articles = scraper.scrape()
```

## Adding New Scrapers

1. **Create scraper class**: Inherit from `BaseBlogScraper`
2. **Implement required methods**: `select_posts()` and `parse_post()`
3. **Add to registry**: Update `scraper/__init__.py`
4. **Add configuration**: Update `config/settings.py` if needed

## Configuration

Scrapers can be configured through:
- **Environment variables**: For API keys and settings
- **Settings file**: `config/settings.py` for defaults
- **Constants**: `utils/constants.py` for categories and rules 