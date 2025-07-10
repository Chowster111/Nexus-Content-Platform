"""
Configuration management for the Engineering Blog Recommender API.

This module provides environment-specific configurations for development, staging,
and production environments. It handles secrets, feature flags, and environment
settings in a secure and maintainable way.
"""

import os
from typing import Optional, Dict, Any
from enum import Enum
from pydantic import BaseSettings, Field


class Environment(str, Enum):
    """Environment types."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DatabaseConfig(BaseSettings):
    """Database configuration settings."""
    
    # Supabase Configuration
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_service_role: str = Field(..., env="SUPABASE_SERVICE_ROLE")
    supabase_anon_key: Optional[str] = Field(None, env="SUPABASE_ANON_KEY")
    
    # Connection Settings
    connection_timeout: int = Field(30, env="DB_CONNECTION_TIMEOUT")
    max_retries: int = Field(3, env="DB_MAX_RETRIES")
    retry_delay: int = Field(1, env="DB_RETRY_DELAY")
    
    class Config:
        env_file = ".env"


class APIConfig(BaseSettings):
    """API configuration settings."""
    
    # Server Settings
    host: str = Field("0.0.0.0", env="API_HOST")
    port: int = Field(8000, env="API_PORT")
    workers: int = Field(1, env="API_WORKERS")
    
    # CORS Settings
    cors_origins: list = Field(["*"], env="CORS_ORIGINS")
    cors_credentials: bool = Field(True, env="CORS_CREDENTIALS")
    
    # Rate Limiting
    rate_limit_requests: int = Field(100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(60, env="RATE_LIMIT_WINDOW")
    
    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    class Config:
        env_file = ".env"


class MLConfig(BaseSettings):
    """Machine Learning configuration settings."""
    
    # Hugging Face
    hf_api_token: Optional[str] = Field(None, env="HF_API_TOKEN")
    
    # OpenRouter (for summarization)
    openrouter_api_key: Optional[str] = Field(None, env="OPENROUTER_API_KEY")
    openrouter_model: str = Field("mistralai/mistral-7b-instruct", env="OPENROUTER_MODEL")
    
    # Embedding Settings
    embedding_model: str = Field("BAAI/bge-small-en-v1.5", env="EMBEDDING_MODEL")
    max_sequence_length: int = Field(512, env="MAX_SEQUENCE_LENGTH")
    tokenizers_parallelism: bool = Field(False, env="TOKENIZERS_PARALLELISM")
    
    # Recommendation Settings
    recommendation_top_k: int = Field(10, env="RECOMMENDATION_TOP_K")
    similarity_threshold: float = Field(0.5, env="SIMILARITY_THRESHOLD")
    
    class Config:
        env_file = ".env"


class ScraperConfig(BaseSettings):
    """Scraper configuration settings."""
    
    # Selenium Settings
    selenium_headless: bool = Field(True, env="SELENIUM_HEADLESS")
    selenium_timeout: int = Field(30, env="SELENIUM_TIMEOUT")
    selenium_implicit_wait: int = Field(10, env="SELENIUM_IMPLICIT_WAIT")
    
    # Rate Limiting
    scraper_delay: float = Field(1.0, env="SCRAPER_DELAY")
    max_articles_per_source: int = Field(50, env="MAX_ARTICLES_PER_SOURCE")
    
    # Retry Settings
    max_retries: int = Field(3, env="SCRAPER_MAX_RETRIES")
    retry_delay: float = Field(2.0, env="SCRAPER_RETRY_DELAY")
    
    # Supported Sources
    enabled_sources: list = Field([
        "netflix", "airbnb", "uber", "stripe", "tinder",
        "doordash", "slack", "notion", "meta", "robinhood"
    ], env="ENABLED_SOURCES")
    
    class Config:
        env_file = ".env"


class MonitoringConfig(BaseSettings):
    """Monitoring and observability configuration."""
    
    # Prometheus
    prometheus_enabled: bool = Field(True, env="PROMETHEUS_ENABLED")
    prometheus_port: int = Field(9090, env="PROMETHEUS_PORT")
    
    # Logging
    log_level: LogLevel = Field(LogLevel.INFO, env="LOG_LEVEL")
    log_format: str = Field("json", env="LOG_FORMAT")
    log_file: Optional[str] = Field(None, env="LOG_FILE")
    
    # Sentry (Error Tracking)
    sentry_dsn: Optional[str] = Field(None, env="SENTRY_DSN")
    sentry_environment: str = Field("development", env="SENTRY_ENVIRONMENT")
    sentry_traces_sample_rate: float = Field(0.1, env="SENTRY_TRACES_SAMPLE_RATE")
    
    # Health Checks
    health_check_interval: int = Field(30, env="HEALTH_CHECK_INTERVAL")
    health_check_timeout: int = Field(10, env="HEALTH_CHECK_TIMEOUT")
    
    class Config:
        env_file = ".env"


class FeatureFlags(BaseSettings):
    """Feature flags for controlling functionality."""
    
    # Core Features
    enable_search: bool = Field(True, env="ENABLE_SEARCH")
    enable_recommendations: bool = Field(True, env="ENABLE_RECOMMENDATIONS")
    enable_scraping: bool = Field(True, env="ENABLE_SCRAPING")
    enable_analytics: bool = Field(True, env="ENABLE_ANALYTICS")
    
    # Advanced Features
    enable_semantic_search: bool = Field(True, env="ENABLE_SEMANTIC_SEARCH")
    enable_personalization: bool = Field(True, env="ENABLE_PERSONALIZATION")
    enable_auto_tagging: bool = Field(True, env="ENABLE_AUTO_TAGGING")
    enable_summarization: bool = Field(True, env="ENABLE_SUMMARIZATION")
    
    # Performance Features
    enable_caching: bool = Field(True, env="ENABLE_CACHING")
    enable_compression: bool = Field(True, env="ENABLE_COMPRESSION")
    enable_rate_limiting: bool = Field(True, env="ENABLE_RATE_LIMITING")
    
    class Config:
        env_file = ".env"


class Settings(BaseSettings):
    """Main application settings."""
    
    # Environment
    environment: Environment = Field(Environment.DEVELOPMENT, env="ENVIRONMENT")
    debug: bool = Field(False, env="DEBUG")
    
    # Application Info
    app_name: str = Field("Engineering Blog Recommender API", env="APP_NAME")
    app_version: str = Field("1.0.0", env="APP_VERSION")
    app_description: str = Field("AI-powered engineering blog recommendation system", env="APP_DESCRIPTION")
    
    # Configurations
    database: DatabaseConfig = DatabaseConfig()
    api: APIConfig = APIConfig()
    ml: MLConfig = MLConfig()
    scraper: ScraperConfig = ScraperConfig()
    monitoring: MonitoringConfig = MonitoringConfig()
    features: FeatureFlags = FeatureFlags()
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings based on environment."""
    return Settings()


def get_environment() -> Environment:
    """Get current environment."""
    env = os.getenv("ENVIRONMENT", "development").lower()
    try:
        return Environment(env)
    except ValueError:
        return Environment.DEVELOPMENT


def is_development() -> bool:
    """Check if running in development environment."""
    return get_environment() == Environment.DEVELOPMENT


def is_staging() -> bool:
    """Check if running in staging environment."""
    return get_environment() == Environment.STAGING


def is_production() -> bool:
    """Check if running in production environment."""
    return get_environment() == Environment.PRODUCTION


def get_log_level() -> str:
    """Get appropriate log level for current environment."""
    env = get_environment()
    if env == Environment.DEVELOPMENT:
        return "DEBUG"
    elif env == Environment.STAGING:
        return "INFO"
    else:
        return "WARNING"


def get_cors_origins() -> list:
    """Get CORS origins based on environment."""
    env = get_environment()
    if env == Environment.DEVELOPMENT:
        return ["http://localhost:3000", "http://localhost:3001", "*"]
    elif env == Environment.STAGING:
        return ["https://staging.engineeringblogrecommender.com"]
    else:
        return ["https://engineeringblogrecommender.com"]


def get_rate_limits() -> Dict[str, int]:
    """Get rate limits based on environment."""
    env = get_environment()
    if env == Environment.DEVELOPMENT:
        return {
            "search": 1000,
            "recommendations": 500,
            "articles": 2000,
            "scraping": 100,
            "analytics": 300
        }
    elif env == Environment.STAGING:
        return {
            "search": 500,
            "recommendations": 250,
            "articles": 1000,
            "scraping": 50,
            "analytics": 150
        }
    else:
        return {
            "search": 100,
            "recommendations": 50,
            "articles": 200,
            "scraping": 10,
            "analytics": 30
        }


# Global settings instance
settings = get_settings() 