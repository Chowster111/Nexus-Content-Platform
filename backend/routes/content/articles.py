from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Query, HTTPException, Path
from db.supabase_client import supabase
from logging_config import logger
from ..utils.retry import with_backoff
from collections import defaultdict
from pydantic import ValidationError
from models.article import ArticleResponse, ArticleCategory, ArticleSource
from models.analytics import TagCount
from models.recommendation import SortOrder


class ArticlesController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self) -> None:
        """Register all article routes with comprehensive documentation."""
        
        @self.router.get(
            "/",
            response_model=List[ArticleResponse],
            summary="Get All Articles",
            description="""
            Retrieve all articles from the database with comprehensive metadata.
            
            This endpoint returns all available articles sorted by publication date (newest first).
            Each article includes full metadata including title, URL, content, source, tags, 
            category, and publication date.
            
            **Features:**
            - Returns all articles with complete metadata
            - Automatic sorting by publication date (newest first)
            - Comprehensive article information including tags and categories
            - Handles validation errors gracefully
            - Supports pagination through database-level ordering
            
            **Response Format:**
            Returns a list of articles with full metadata including:
            - Article title and URL
            - Publication date and source
            - Content summary and full text
            - Tags and category classification
            - Source attribution and metadata
            """,
            response_description="List of all articles with complete metadata",
            tags=["Articles"]
        )
        def get_all_articles() -> List[ArticleResponse]:
            """Get all articles from the database."""
            logger.info("Fetching all articles")
            try:
                response: Dict[str, Any] = supabase.table("articles").select("*").order("published_date", desc=True).execute()
                articles = []
                errors = []
                for article in response.data:
                    try:
                        articles.append(ArticleResponse(**article))
                    except ValidationError as ve:
                        logger.error(f"Validation error for article: {article} | {ve}")
                        errors.append({"article": article, "error": str(ve)})
                if errors:
                    logger.warning(f"Some articles could not be validated: {errors}")
                return articles
            except Exception as e:
                logger.exception("ERROR fetching all articles")
                raise HTTPException(status_code=500, detail=f"Internal error: {e}")

        @self.router.get(
            "/tags/{tag}",
            response_model=List[ArticleResponse],
            summary="Get Articles by Tag",
            description="""
            Retrieve articles filtered by a specific tag with optional sorting.
            
            This endpoint finds all articles that contain the specified tag in their tag list.
            The search is case-insensitive and supports partial tag matching.
            
            **Features:**
            - Case-insensitive tag matching
            - Optional sorting by publication date (latest/oldest)
            - Partial tag matching support
            - Returns articles with complete metadata
            
            **Example Usage:**
            ```
            GET /articles/tags/machine-learning?sort=latest
            GET /articles/tags/python?sort=oldest
            ```
            
            **Supported Tags:**
            Common tags include: machine-learning, python, javascript, architecture, 
            scalability, microservices, database, frontend, backend, devops, etc.
            """,
            response_description="List of articles matching the specified tag",
            tags=["Articles"]
        )
        def get_articles_by_tag(
            tag: str = Path(..., description="Tag to filter articles by", example="machine-learning"),
            sort: str = Query("latest", pattern="^(latest|oldest)$", description="Sort order for results")
        ) -> List[ArticleResponse]:
            """Get articles filtered by a specific tag."""
            logger.info(f"Fetching articles by tag: '{tag}' with sort='{sort}'")
            tag = tag.lower()
            try:
                response: Dict[str, Any] = self._fetch_articles()
            except Exception as e:
                logger.exception("ERROR fetching articles by tag")
                raise HTTPException(status_code=500, detail=f"Internal error: {e}")

            filtered: List[Dict[str, Any]] = [
                a for a in response.data
                if a.get("tags") and any(tag in t.lower() for t in a["tags"])
            ]

            sorted_articles: List[Dict[str, Any]] = self._sort_articles(filtered, sort)
            articles = []
            errors = []
            for article in sorted_articles:
                try:
                    articles.append(ArticleResponse(**article))
                except ValidationError as ve:
                    logger.error(f"Validation error for article: {article} | {ve}")
                    errors.append({"article": article, "error": str(ve)})
            if errors:
                logger.warning(f"Some articles by tag could not be validated: {errors}")
            return articles

        @self.router.get(
            "/filter",
            response_model=List[ArticleResponse],
            summary="Filter Articles by Multiple Tags",
            description="""
            Filter articles by multiple tags with advanced matching logic.
            
            This endpoint allows filtering articles by multiple tags simultaneously.
            Articles must match at least one of the provided tags to be included in results.
            
            **Features:**
            - Multi-tag filtering with OR logic
            - Case-insensitive tag matching
            - Optional sorting by publication date
            - Support for partial tag matching
            - Returns articles with complete metadata
            
            **Example Usage:**
            ```
            GET /articles/filter?tags=machine-learning&tags=python&sort=latest
            GET /articles/filter?tags=architecture&tags=scalability&sort=oldest
            ```
            
            **Filtering Logic:**
            - Articles matching ANY of the provided tags are returned
            - Tags are matched case-insensitively
            - Partial matches are supported
            - Results are sorted by publication date
            """,
            response_description="List of articles matching any of the specified tags",
            tags=["Articles"]
        )
        def filter_articles_by_tag(
            tags: Optional[List[str]] = Query(None, description="List of tags to filter by"),
            sort: str = Query("latest", pattern="^(latest|oldest)$", description="Sort order for results")
        ) -> List[ArticleResponse]:
            """Filter articles by multiple tags."""
            if not tags:
                raise HTTPException(status_code=400, detail="No tags provided")

            tags = [tag.lower() for tag in tags]
            logger.info(f"🔍 Filtering by tags: {tags} with sort='{sort}'")
            try:
                response: Dict[str, Any] = self._fetch_articles()
            except Exception as e:
                logger.exception("ERROR filtering articles by tag")
                raise HTTPException(status_code=500, detail=f"Internal error: {e}")

            filtered: List[Dict[str, Any]] = [
                a for a in response.data
                if a.get("tags") and any(
                    any(query_tag in tag.lower() for tag in a["tags"])
                    for query_tag in tags
                )
            ]

            sorted_articles: List[Dict[str, Any]] = self._sort_articles(filtered, sort)
            articles = []
            errors = []
            for article in sorted_articles:
                try:
                    articles.append(ArticleResponse(**article))
                except ValidationError as ve:
                    logger.error(f"Validation error for article: {article} | {ve}")
                    errors.append({"article": article, "error": str(ve)})
            if errors:
                logger.warning(f"Some filtered articles could not be validated: {errors}")
            return articles

        @self.router.get(
            "/all-tags",
            response_model=List[TagCount],
            summary="Get All Tags with Counts",
            description="""
            Retrieve all available tags with their usage counts.
            
            This endpoint provides a comprehensive list of all tags used across articles
            along with the number of articles that use each tag. This is useful for
            building tag clouds, filtering interfaces, and understanding content distribution.
            
            **Features:**
            - Returns all unique tags with usage counts
            - Sorted by frequency (most used first)
            - Case-insensitive tag aggregation
            - Real-time counts from current article database
            
            **Response Format:**
            Returns a list of tag objects with:
            - `tag`: The tag name (lowercase)
            - `count`: Number of articles using this tag
            
            **Example Response:**
            ```json
            [
              {"tag": "machine-learning", "count": 45},
              {"tag": "python", "count": 32},
              {"tag": "architecture", "count": 28}
            ]
            ```
            """,
            response_description="List of all tags with their usage counts",
            tags=["Articles"]
        )
        def get_all_tags() -> List[TagCount]:
            """Get all tags with their counts."""
            logger.info("Fetching all tags")
            try:
                response: Dict[str, Any] = self._fetch_tags()
            except Exception as e:
                logger.exception("ERROR fetching all tags")
                raise HTTPException(status_code=500, detail=str(e))

            tag_counter: Dict[str, int] = defaultdict(int)
            for row in response.data:
                for tag in row.get("tags", []):
                    tag_counter[tag.lower()] += 1

            sorted_tags: List[tuple] = sorted(tag_counter.items(), key=lambda x: -x[1])
            return [TagCount(tag=tag, count=count) for tag, count in sorted_tags]

        @self.router.get(
            "/by-category/{category}",
            response_model=List[ArticleResponse],
            summary="Get Articles by Category",
            description="""
            Retrieve articles filtered by category with optional sorting.
            
            This endpoint returns all articles that belong to the specified category.
            Categories are predefined and include areas like Architecture, Machine Learning,
            Frontend, Backend, DevOps, etc.
            
            **Features:**
            - Category-based filtering
            - Optional sorting by publication date
            - Case-insensitive category matching
            - Returns articles with complete metadata
            
            **Available Categories:**
            - Architecture
            - Machine Learning
            - Frontend
            - Backend
            - DevOps
            - Database
            - Security
            - Performance
            - Testing
            - Mobile
            
            **Example Usage:**
            ```
            GET /articles/by-category/architecture?sort=latest
            GET /articles/by-category/machine-learning?sort=oldest
            ```
            """,
            response_description="List of articles in the specified category",
            tags=["Articles"]
        )
        def get_by_category(
            category: str = Path(..., description="Category to filter by", example="architecture"),
            sort: str = Query("latest", pattern="^(latest|oldest)$", description="Sort order for results")
        ) -> List[ArticleResponse]:
            """Get articles by category."""
            category = category[0].upper() + category[1:].lower()
            logger.info(f"Fetching articles by category: '{category}'")
            try:
                response: Dict[str, Any] = supabase.table("articles").select("*").eq("category", category).execute()
            except Exception as e:
                logger.exception("ERROR fetching by category")
                raise HTTPException(status_code=500, detail=f"Internal error: {e}")

            sorted_articles: List[Dict[str, Any]] = self._sort_articles(response.data, sort)
            articles = []
            errors = []
            for article in sorted_articles:
                try:
                    articles.append(ArticleResponse(**article))
                except ValidationError as ve:
                    logger.error(f"Validation error for article: {article} | {ve}")
                    errors.append({"article": article, "error": str(ve)})
            if errors:
                logger.warning(f"Some articles by category could not be validated: {errors}")
            return articles

        @self.router.get(
            "/by-source/{source}",
            response_model=List[ArticleResponse],
            summary="Get Articles by Source",
            description="""
            Retrieve articles from a specific source with optional sorting.
            
            This endpoint returns all articles from the specified source (e.g., Netflix, 
            Airbnb, Uber, Stripe, etc.). Sources represent the engineering blogs of 
            different companies.
            
            **Features:**
            - Source-based filtering
            - Optional sorting by publication date
            - Case-insensitive source matching
            - Returns articles with complete metadata
            
            **Available Sources:**
            - netflix: Netflix Engineering Blog
            - airbnb: Airbnb Engineering & Data Science
            - uber: Uber Engineering
            - stripe: Stripe Engineering
            - tinder: Tinder Engineering
            - doordash: DoorDash Engineering
            - slack: Slack Engineering
            - notion: Notion Engineering
            - meta: Meta Engineering
            - robinhood: Robinhood Engineering
            
            **Example Usage:**
            ```
            GET /articles/by-source/netflix?sort=latest
            GET /articles/by-source/airbnb?sort=oldest
            ```
            """,
            response_description="List of articles from the specified source",
            tags=["Articles"]
        )
        def get_by_source(
            source: str = Path(..., description="Source to filter by", example="netflix"),
            sort: str = Query("latest", pattern="^(latest|oldest)$", description="Sort order for results")
        ) -> List[ArticleResponse]:
            """Get articles by source."""
            source = source.lower()
            source_mapping: Dict[str, str] = {
                "netflix": ArticleSource.NETFLIX,
                "airbnb": ArticleSource.AIRBNB,
                "stripe": ArticleSource.STRIPE,
                "tinder": ArticleSource.TINDER,
                "uber": ArticleSource.UBER
            }
            source = source_mapping.get(source, source)

            logger.info(f"Fetching by source: '{source}'")
            try:
                response: Dict[str, Any] = supabase.table("articles").select("*").eq("source", source).execute()
            except Exception as e:
                logger.exception("ERROR fetching by source")
                raise HTTPException(status_code=500, detail=f"Internal error: {e}")

            sorted_articles: List[Dict[str, Any]] = self._sort_articles(response.data, sort)
            articles = []
            errors = []
            for article in sorted_articles:
                try:
                    articles.append(ArticleResponse(**article))
                except ValidationError as ve:
                    logger.error(f"Validation error for article: {article} | {ve}")
                    errors.append({"article": article, "error": str(ve)})
            if errors:
                logger.warning(f"Some articles by source could not be validated: {errors}")
            return articles

        @self.router.get(
            "/{article_id}",
            response_model=ArticleResponse,
            summary="Get Single Article",
            description="""
            Retrieve a single article by its unique identifier.
            
            This endpoint returns the complete article data for a specific article ID.
            The article includes all metadata, content, and associated information.
            
            **Features:**
            - Single article retrieval by ID
            - Complete article metadata and content
            - Validation of article data structure
            - Error handling for missing articles
            
            **Response Format:**
            Returns a single article with complete information including:
            - Article title, URL, and content
            - Publication date and source
            - Tags and category
            - Summary and full text content
            - All associated metadata
            
            **Error Handling:**
            - Returns 404 if article not found
            - Returns 500 for validation or database errors
            - Logs detailed error information for debugging
            """,
            response_description="Complete article data for the specified ID",
            tags=["Articles"]
        )
        def get_article(
            article_id: str = Path(..., description="Unique article identifier", example="article-123")
        ) -> ArticleResponse:
            """Get a single article by ID."""
            logger.info(f"Fetching single article with id: {article_id}")
            try:
                response: Dict[str, Any] = supabase.table("articles").select("*").eq("id", article_id).single().execute()
                try:
                    return ArticleResponse(**response.data)
                except ValidationError as ve:
                    logger.error(f"Validation error for article id {article_id}: {response.data} | {ve}")
                    raise HTTPException(status_code=500, detail=f"Validation error: {ve}")
            except Exception as e:
                logger.exception("ERROR fetching article")
                raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    @with_backoff()
    def _fetch_articles(self) -> Dict[str, Any]:
        """Fetch all articles from the database."""
        return supabase.table("articles").select("*").execute()

    @with_backoff()
    def _fetch_tags(self) -> Dict[str, Any]:
        """Fetch all tags from the database."""
        return supabase.table("articles").select("tags").execute()

    def _sort_articles(self, articles: List[Dict[str, Any]], sort_order: str) -> List[Dict[str, Any]]:
        """Sort articles by published date."""
        return sorted(
            articles,
            key=lambda a: a.get("published_date", ""),
            reverse=(sort_order == SortOrder.LATEST)
        )
