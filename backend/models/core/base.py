"""
Base models and common types for the application.

This module contains base classes and common types used across the application.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class BaseEntity(BaseModel):
    """Base class for all domain entities."""
    
    id: Optional[str] = Field(None, description="Unique identifier")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True


class BaseResponse(BaseModel):
    """Base class for API responses."""
    
    success: bool = Field(..., description="Whether the operation was successful")
    message: Optional[str] = Field(None, description="Response message")
    error: Optional[str] = Field(None, description="Error message if operation failed")
    
    class Config:
        from_attributes = True


class PaginationParams(BaseModel):
    """Common pagination parameters."""
    
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(10, ge=1, le=100, description="Items per page")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries."""
        return (self.page - 1) * self.limit


class SortParams(BaseModel):
    """Common sorting parameters."""
    
    sort_by: Optional[str] = Field(None, description="Field to sort by")
    sort_order: str = Field("desc", pattern="^(asc|desc)$", description="Sort order")


class FilterParams(BaseModel):
    """Common filtering parameters."""
    
    filters: Optional[Dict[str, Any]] = Field(None, description="Filter criteria")
    search: Optional[str] = Field(None, description="Search query") 