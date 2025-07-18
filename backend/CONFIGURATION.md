# Configuration Management

This document describes the comprehensive configuration management system for the Engineering Blog Recommender API, which supports multiple environments with environment-specific settings.

## Overview

The configuration system uses Pydantic's `BaseSettings` to provide type-safe, environment-specific configurations with the following features:

- **Environment Detection**: Automatic detection of development, staging, and production environments
- **Feature Flags**: Enable/disable features per environment
- **Security**: Environment-specific security settings
- **Performance**: Optimized settings for each environment
- **Monitoring**: Environment-specific logging and monitoring

## Environment Types

### Development Environment
- **Purpose**: Local development and testing
- **Features**: All features enabled, debug mode, verbose logging
- **Security**: Relaxed settings for development
- **Performance**: Optimized for development speed

### Staging Environment
- **Purpose**: Pre-production testing and validation
- **Features**: Most features enabled, moderate logging
- **Security**: Production-like security settings
- **Performance**: Balanced performance and monitoring

### Production Environment
- **Purpose**: Live production deployment
- **Features**: Conservative feature set, minimal logging
- **Security**: Strict security settings
- **Performance**: Optimized for production stability

## Configuration Structure

### Core Configuration Classes

#### `DatabaseConfig`
Database connection and Supabase settings:
```python
class DatabaseConfig(BaseSettings):
    supabase_url: str
    supabase_service_role: str
    supabase_anon_key: Optional[str]
    connection_timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 1
```

#### `APIConfig`
API server and security settings:
```python
class APIConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    cors_origins: list = ["*"]
    rate_limit_requests: int = 100
    secret_key: str
    algorithm: str = "HS256"
```

#### `MLConfig`
Machine learning and AI settings:
```python
class MLConfig(BaseSettings):
    hf_api_token: Optional[str]
    openrouter_api_key: Optional[str]
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    recommendation_top_k: int = 10
    similarity_threshold: float = 0.5
```

#### `ScraperConfig`
Web scraping settings:
```python
class ScraperConfig(BaseSettings):
    selenium_headless: bool = True
    selenium_timeout: int = 30
    scraper_delay: float = 1.0
    max_articles_per_source: int = 50
    enabled_sources: list
```

#### `MonitoringConfig`
Logging and monitoring settings:
```python
class MonitoringConfig(BaseSettings):
    prometheus_enabled: bool = True
    log_level: LogLevel = LogLevel.INFO
    sentry_dsn: Optional[str]
    health_check_interval: int = 30
```

#### `FeatureFlags`
Feature enable/disable settings:
```python
class FeatureFlags(BaseSettings):
    enable_search: bool = True
    enable_recommendations: bool = True
    enable_scraping: bool = True
    enable_analytics: bool = True
    enable_semantic_search: bool = True
    enable_personalization: bool = True
```

## Environment-Specific Settings

### Development Environment

**File**: `env.development.example` → `.env`

**Key Settings**:
- `ENVIRONMENT=development`
- `DEBUG=true`
- `LOG_LEVEL=DEBUG`
- `RATE_LIMIT_REQUESTS=1000`
- All features enabled
- Relaxed CORS settings

**Usage**:
```bash
cp env.development.example .env
# Edit .env with your local values
```

### Staging Environment

**File**: `env.staging.example` → `.env.staging`

**Key Settings**:
- `ENVIRONMENT=staging`
- `DEBUG=false`
- `LOG_LEVEL=INFO`
- `RATE_LIMIT_REQUESTS=500`
- Most features enabled
- Restricted CORS settings

**Usage**:
```bash
cp env.staging.example .env.staging
# Edit .env.staging with staging values
```

### Production Environment

**File**: `env.production.example` → `.env.production`

**Key Settings**:
- `ENVIRONMENT=production`
- `DEBUG=false`
- `LOG_LEVEL=WARNING`
- `RATE_LIMIT_REQUESTS=100`
- Conservative feature set
- Strict CORS settings

**Usage**:
```bash
cp env.production.example .env.production
# Edit .env.production with production values
```

## Environment Variables

### Required Variables

#### Database
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_SERVICE_ROLE`: Supabase service role key
- `SUPABASE_ANON_KEY`: Supabase anonymous key (optional)

#### Security
- `SECRET_KEY`: Secret key for JWT tokens
- `JWT_ALGORITHM`: JWT algorithm (default: HS256)

#### API Keys
- `HF_API_TOKEN`: Hugging Face API token (optional)
- `OPENROUTER_API_KEY`: OpenRouter API key (optional)

### Optional Variables

#### Performance
- `API_WORKERS`: Number of worker processes
- `DB_CONNECTION_TIMEOUT`: Database connection timeout
- `DB_MAX_RETRIES`: Database retry attempts

#### Monitoring
- `SENTRY_DSN`: Sentry error tracking DSN
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `PROMETHEUS_ENABLED`: Enable Prometheus metrics

#### Feature Flags
- `ENABLE_SEARCH`: Enable search functionality
- `ENABLE_RECOMMENDATIONS`: Enable recommendations
- `ENABLE_SCRAPING`: Enable web scraping
- `ENABLE_ANALYTICS`: Enable analytics

## Usage in Code

### Basic Usage

```python
from config import settings, get_environment

# Access configuration
database_url = settings.database.supabase_url
log_level = settings.monitoring.log_level

# Check environment
if get_environment() == "development":
    # Development-specific code
    pass
```

### Environment-Specific Logic

```python
from config import is_development, is_production, get_rate_limits

# Get environment-specific rate limits
rate_limits = get_rate_limits()

# Environment-specific behavior
if is_development():
    # Development logic
    pass
elif is_production():
    # Production logic
    pass
```

### Feature Flags

```python
from config import settings

# Check if features are enabled
if settings.features.enable_search:
    # Initialize search functionality
    pass

if settings.features.enable_scraping:
    # Initialize scraper
    pass
```

## Docker Configuration

### Development
```yaml
# docker-compose.yml
services:
  backend:
    env_file:
      - .env
```

### Production
```yaml
# docker-compose.prod.yml
services:
  backend:
    env_file:
      - .env.production
```

## AWS ECS Configuration

### Environment Variables in ECS Task Definition

```json
{
  "environment": [
    {
      "name": "ENVIRONMENT",
      "value": "production"
    },
    {
      "name": "SUPABASE_URL",
      "value": "https://your-project.supabase.co"
    }
  ],
  "secrets": [
    {
      "name": "SUPABASE_SERVICE_ROLE",
      "valueFrom": "arn:aws:secretsmanager:region:account:secret:supabase-service-role"
    }
  ]
}
```

## Security Best Practices

### Development
- Use `.env` files for local development
- Never commit `.env` files to version control
- Use placeholder values in example files

### Staging
- Use environment variables in container orchestration
- Use separate Supabase project for staging
- Enable moderate logging for debugging

### Production
- Use AWS Secrets Manager for sensitive values
- Use IAM roles for container authentication
- Minimize logging to reduce overhead
- Use separate Supabase project for production

## Monitoring and Observability

### Environment-Specific Monitoring

#### Development
- Debug logging enabled
- Prometheus metrics available
- Health checks every 30 seconds
- Full error tracking

#### Staging
- Info logging enabled
- Prometheus metrics available
- Health checks every 30 seconds
- Error tracking with sampling

#### Production
- Warning logging only
- Prometheus metrics available
- Health checks every 30 seconds
- Minimal error tracking

### Health Check Integration

```python
from config import settings

def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
        "features": {
            "search": settings.features.enable_search,
            "recommendations": settings.features.enable_recommendations,
            "scraping": settings.features.enable_scraping,
            "analytics": settings.features.enable_analytics,
        }
    }
```

## Troubleshooting

### Common Issues

1. **Configuration Not Loading**
   - Check if `.env` file exists
   - Verify environment variable names
   - Check file permissions

2. **Database Connection Issues**
   - Verify Supabase credentials
   - Check network connectivity
   - Validate URL format

3. **Feature Flags Not Working**
   - Check environment variable values
   - Verify boolean parsing
   - Check default values

### Debug Commands

```bash
# Check current environment
echo $ENVIRONMENT

# Test configuration loading
python -c "from config import settings; print(settings.environment)"

# Test database connection
python -c "from db.supabase_client import test_connection; print(test_connection())"
```

## Migration Guide

### From Basic Configuration

If you're migrating from the basic configuration system:

1. **Update imports**:
   ```python
   # Old
   from dotenv import load_dotenv
   import os
   
   # New
   from config import settings
   ```

2. **Replace environment variable access**:
   ```python
   # Old
   SUPABASE_URL = os.getenv("SUPABASE_URL")
   
   # New
   supabase_url = settings.database.supabase_url
   ```

3. **Add environment-specific logic**:
   ```python
   from config import get_environment
   
   if get_environment() == "production":
       # Production-specific code
       pass
   ```

## Future Enhancements

### Planned Features

1. **Configuration Validation**: Add schema validation for configuration
2. **Hot Reloading**: Support configuration changes without restart
3. **Configuration UI**: Web interface for configuration management
4. **Configuration Backup**: Automatic backup of configuration settings
5. **Configuration Migration**: Tools for migrating between environments

### Contributing

When adding new configuration options:

1. Add to appropriate configuration class
2. Update environment example files
3. Add documentation
4. Add validation if needed
5. Update tests

## Support

For configuration issues:

1. Check the environment-specific example files
2. Verify environment variable names
3. Test configuration loading
4. Check logs for configuration errors
5. Review this documentation

---

This configuration system provides a robust, scalable foundation for managing environment-specific settings across development, staging, and production deployments. 