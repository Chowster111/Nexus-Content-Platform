"""
Health check models for system monitoring.

This module contains Pydantic models for health check responses
and system status monitoring.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoints."""
    
    status: str = Field(..., description="Overall system status (ok, degraded, fail)")
    database: str = Field(..., description="Database connection status")
    latency_ms: float = Field(..., description="Response latency in milliseconds")
    error: Optional[str] = Field(None, description="Error message if health check failed")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional health check details")
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['ok', 'degraded', 'fail']
        if v not in valid_statuses:
            raise ValueError(f"status must be one of {valid_statuses}")
        return v
    
    @validator('latency_ms')
    def validate_latency(cls, v):
        if v < 0:
            raise ValueError("latency_ms cannot be negative")
        return v


class SystemStatus(BaseModel):
    """Model for system component status."""
    
    component: str = Field(..., description="Component name")
    status: str = Field(..., description="Component status")
    response_time: Optional[float] = Field(None, description="Component response time")
    error: Optional[str] = Field(None, description="Component error message")
    
    @validator('status')
    def validate_component_status(cls, v):
        valid_statuses = ['ok', 'degraded', 'fail', 'unknown']
        if v not in valid_statuses:
            raise ValueError(f"status must be one of {valid_statuses}")
        return v


class DetailedHealthResponse(BaseModel):
    """Detailed health check response with component breakdown."""
    
    overall_status: str = Field(..., description="Overall system status")
    latency_ms: float = Field(..., description="Total response latency")
    components: Dict[str, SystemStatus] = Field(default_factory=dict, description="Component statuses")
    timestamp: Optional[str] = Field(None, description="Health check timestamp")
    
    @validator('overall_status')
    def validate_overall_status(cls, v):
        valid_statuses = ['ok', 'degraded', 'fail']
        if v not in valid_statuses:
            raise ValueError(f"overall_status must be one of {valid_statuses}")
        return v 