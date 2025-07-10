"""
Unit tests for Pydantic models validation.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from models.likes import LikeRequest, LikeResponse, LikeRecord
from models.search import SearchResult, SearchResponse, SearchRequest


class TestLikesModels:
    """Test cases for likes-related models."""
    
    def test_like_request_valid(self):
        """Test valid LikeRequest creation."""
        like_request = LikeRequest(
            article_id="test-article-123",
            user_id="test-user-456",
            url="https://example.com/article",
            liked=True
        )
        assert like_request.article_id == "test-article-123"
        assert like_request.user_id == "test-user-456"
        assert like_request.liked is True
    
    def test_like_request_invalid_empty_fields(self):
        """Test LikeRequest validation with empty fields."""
        with pytest.raises(ValidationError):
            LikeRequest(
                article_id="",
                user_id="test-user",
                liked=True
            )
        
        with pytest.raises(ValidationError):
            LikeRequest(
                article_id="test-article",
                user_id="",
                liked=True
            )
    
    def test_like_response_valid(self):
        """Test valid LikeResponse creation."""
        response = LikeResponse(
            message="Likes saved successfully",
            liked=True,
            count=5
        )
        assert response.message == "Likes saved successfully"
        assert response.liked is True
        assert response.count == 5
    
    def test_like_record_valid(self):
        """Test valid LikeRecord creation."""
        record = LikeRecord(
            user_id="test-user",
            article_url="https://example.com/article",
            liked=True,
            created_at=datetime.now()
        )
        assert record.user_id == "test-user"
        assert record.article_url == "https://example.com/article"
        assert record.liked is True


class TestSearchModels:
    """Test cases for search-related models."""
    
    def test_search_result_valid(self):
        """Test valid SearchResult creation."""
        result = SearchResult(
            title="Test Article",
            url="https://example.com/article",
            published_date=datetime.now(),
            content="This is test content",
            source="example.com",
            tags=["python", "testing"],
            category="technology",
            summary="A test article"
        )
        assert result.title == "Test Article"
        assert result.url == "https://example.com/article"
        assert result.tags == ["python", "testing"]
    
    def test_search_result_invalid_url(self):
        """Test SearchResult validation with invalid URL."""
        with pytest.raises(ValidationError):
            SearchResult(
                title="Test Article",
                url="not-a-url",
                published_date=datetime.now()
            )
    
    def test_search_result_empty_title(self):
        """Test SearchResult validation with empty title."""
        with pytest.raises(ValidationError):
            SearchResult(
                title="",
                url="https://example.com/article",
                published_date=datetime.now()
            )
    
    def test_search_response_valid(self):
        """Test valid SearchResponse creation."""
        response = SearchResponse(
            results=[],
            query="test query",
            total_count=0
        )
        assert response.results == []
        assert response.query == "test query"
        assert response.total_count == 0
    
    def test_search_response_with_error(self):
        """Test SearchResponse with error."""
        response = SearchResponse(
            results=[],
            error="Search failed"
        )
        assert response.error == "Search failed"
    
    def test_search_request_valid(self):
        """Test valid SearchRequest creation."""
        request = SearchRequest(
            query="python testing",
            limit=20,
            offset=0
        )
        assert request.query == "python testing"
        assert request.limit == 20
        assert request.offset == 0
    
    def test_search_request_invalid_empty_query(self):
        """Test SearchRequest validation with empty query."""
        with pytest.raises(ValidationError):
            SearchRequest(query="")
    
    def test_search_request_invalid_limit(self):
        """Test SearchRequest validation with invalid limit."""
        with pytest.raises(ValidationError):
            SearchRequest(
                query="test",
                limit=0  # Should be >= 1
            )
        
        with pytest.raises(ValidationError):
            SearchRequest(
                query="test",
                limit=101  # Should be <= 100
            ) 