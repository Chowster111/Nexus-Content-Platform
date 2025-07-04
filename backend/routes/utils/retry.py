import time
import functools
import logging

logger = logging.getLogger(__name__)

def with_backoff(max_retries=3, backoff_factor=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            last_error = None  # ✅ Track last exception
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e  # ✅ Save it
                    wait = backoff_factor * (2 ** retries)
                    logger.warning(f"Retry {retries + 1}/{max_retries} after error: {e} (waiting {wait:.1f}s)")
                    time.sleep(wait)
                    retries += 1
            logger.error(f"Exceeded max retries for {func.__name__}")
            if last_error:
                raise last_error  # ✅ Re-raise the actual exception
            else:
                raise RuntimeError("Exceeded retries but no exception captured.")
        return wrapper
    return decorator
