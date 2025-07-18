# db/supabase_client.py
import os
from typing import Optional, Dict, Any
from supabase import create_client, Client
from config import settings
from logging_config import logger

# Initialize Supabase client with configuration
try:
    supabase: Client = create_client(
        settings.database.supabase_url,
        settings.database.supabase_service_role
    )
    logger.info("✅ Supabase client initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize Supabase client: {e}")
    raise

def get_supabase_client() -> Client:
    """Get the configured Supabase client."""
    return supabase

def test_connection() -> bool:
    """Test the database connection."""
    try:
        # Simple query to test connection
        response = supabase.table("articles").select("id").limit(1).execute()
        logger.info("✅ Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection test failed: {e}")
        return False

def get_connection_info() -> Dict[str, Any]:
    """Get database connection information."""
    return {
        "url": settings.database.supabase_url,
        "timeout": settings.database.connection_timeout,
        "max_retries": settings.database.max_retries,
        "retry_delay": settings.database.retry_delay,
        "connected": test_connection()
    }

# No data transformation or model construction is present here, but add a comment for future maintainers.
# If you add any data transformation or model construction here, ensure to add Pydantic validation and error handling.
