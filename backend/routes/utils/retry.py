import time
import functools
import logging

logger = logging.getLogger(__name__)

def with_backoff(max_retries=3, backoff_factor=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    wait = backoff_factor * (2 ** retries)
                    logger.warning(f"Retry {retries + 1}/{max_retries} after error: {e} (waiting {wait:.1f}s)")
                    time.sleep(wait)
                    retries += 1
            logger.error(f"Exceeded max retries for {func.__name__}")
            raise
        return wrapper
    return decorator
