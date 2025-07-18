"""
System monitoring and observability models.

This module contains models for system monitoring, metrics collection, and observability.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class MetricPoint(BaseModel):
    """Individual metric data point."""
    
    timestamp: datetime = Field(..., description="Metric timestamp")
    value: float = Field(..., description="Metric value")
    labels: Optional[Dict[str, str]] = Field(None, description="Metric labels")


class SystemMetric(BaseModel):
    """System metric with multiple data points."""
    
    name: str = Field(..., description="Metric name")
    description: str = Field(..., description="Metric description")
    unit: str = Field(..., description="Metric unit")
    data_points: List[MetricPoint] = Field(default_factory=list, description="Metric data points")
    tags: Optional[Dict[str, str]] = Field(None, description="Metric tags")


class AlertRule(BaseModel):
    """Alert rule configuration."""
    
    name: str = Field(..., description="Alert rule name")
    metric_name: str = Field(..., description="Metric to monitor")
    threshold: float = Field(..., description="Alert threshold")
    operator: str = Field(..., pattern="^(gt|lt|gte|lte|eq)$", description="Comparison operator")
    severity: str = Field(..., pattern="^(info|warning|error|critical)$", description="Alert severity")
    enabled: bool = Field(True, description="Whether alert is enabled")


class Alert(BaseModel):
    """Active alert instance."""
    
    id: str = Field(..., description="Alert identifier")
    rule_name: str = Field(..., description="Triggering rule name")
    severity: str = Field(..., description="Alert severity")
    message: str = Field(..., description="Alert message")
    triggered_at: datetime = Field(..., description="Alert trigger timestamp")
    resolved_at: Optional[datetime] = Field(None, description="Alert resolution timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional alert metadata")


class ServiceStatus(BaseModel):
    """Status of a system service."""
    
    service_name: str = Field(..., description="Service name")
    status: str = Field(..., pattern="^(healthy|degraded|unhealthy|unknown)$", description="Service status")
    response_time: Optional[float] = Field(None, description="Service response time in ms")
    last_check: datetime = Field(..., description="Last health check timestamp")
    error_message: Optional[str] = Field(None, description="Error message if unhealthy")
    dependencies: List[str] = Field(default_factory=list, description="Service dependencies")


class SystemOverview(BaseModel):
    """Overall system status overview."""
    
    overall_status: str = Field(..., description="Overall system status")
    services: List[ServiceStatus] = Field(default_factory=list, description="Service statuses")
    active_alerts: List[Alert] = Field(default_factory=list, description="Active alerts")
    metrics_summary: Dict[str, float] = Field(default_factory=dict, description="Key metrics summary")
    last_updated: datetime = Field(..., description="Last update timestamp") 