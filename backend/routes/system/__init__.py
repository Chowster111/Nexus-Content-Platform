"""
System and infrastructure routes.

This module contains routes for health checks, monitoring, and system management.
"""

from .health import HealthController

__all__ = [
    "HealthController"
] 