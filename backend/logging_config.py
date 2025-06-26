# logging_config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

logger = logging.getLogger("recommender")
logger = logging.getLogger("scraper")
logger = logging.getLogger("search")
logger = logging.getLogger("likes")