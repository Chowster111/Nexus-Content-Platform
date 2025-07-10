from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from db.supabase_client import supabase
from logging_config import logger
import time
from pydantic import ValidationError
from models.health import HealthCheckResponse


class HealthController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self) -> None:
        """Register all health check routes."""
        @self.router.get(
            "/health",
            summary="System Health Check",
            description="""
            Perform a comprehensive health check of the system.
            
            This endpoint provides real-time system health information including database
            connectivity, response latency, and overall system status. It's designed for
            monitoring systems, load balancers, and DevOps tooling.
            
            **Health Check Components:**
            - Database connectivity (Supabase)
            - Response latency measurement
            - System status assessment
            - Error detection and reporting
            
            **Response Statuses:**
            - `ok`: All systems operational
            - `degraded`: Some systems experiencing issues
            - `fail`: Critical system failure
            
            **Database Status:**
            - `ok`: Database accessible and responding
            - `no data`: Database accessible but no data
            - `no response`: Database connectivity issues
            
            **Monitoring Integration:**
            - Compatible with Prometheus monitoring
            - Supports health check endpoints for load balancers
            - Provides detailed error information for debugging
            - Includes response latency for performance monitoring
            
            **Use Cases:**
            - Load balancer health checks
            - Kubernetes liveness/readiness probes
            - Monitoring dashboard integration
            - DevOps automation and alerting
            """,
            response_description="Comprehensive system health status with database connectivity and latency",
            tags=["Health"]
        )
        def health_check() -> Dict[str, Any]:
            """
            Perform a comprehensive health check of the system.
            
            Checks database connectivity, measures response latency, and provides
            overall system status for monitoring and load balancing purposes.
            
            **Response Format:**
            ```json
            {
              "status": "ok|degraded|fail",
              "database": "ok|no_data|no_response",
              "latency_ms": 15.23
            }
            ```
            
            **Example Responses:**
            
            **Healthy System:**
            ```json
            {
              "status": "ok",
              "database": "ok",
              "latency_ms": 12.45
            }
            ```
            
            **Degraded System:**
            ```json
            {
              "status": "degraded",
              "database": "no_data",
              "latency_ms": 45.67
            }
            ```
            
            **Failed System:**
            ```json
            {
              "status": "fail",
              "error": "Database connection timeout",
              "latency_ms": 5000.0
            }
            ```
            
            **Monitoring Integration:**
            - HTTP 200: System healthy or degraded
            - HTTP 500: System failed
            - Response time indicates system performance
            - Database status shows data layer health
            """
            start_time: float = time.time()
            try:
                response: Dict[str, Any] = self.check_database()
                latency_ms: float = round((time.time() - start_time) * 1000, 2)

                db_status: str = self.interpret_db_status(response)
                logger.info(f"HEALTH CHECK: status=ok, db_status={db_status}, latency={latency_ms}ms")

                result = {
                    "status": "ok" if db_status == "ok" else "degraded",
                    "database": db_status,
                    "latency_ms": latency_ms,
                }
                try:
                    # Validate health check response
                    HealthCheckResponse(**result)
                except ValidationError as ve:
                    logger.error(f"Validation error for health check response: {result} | {ve}")
                    raise HTTPException(status_code=500, detail=f"Validation error: {ve}")
                return result
            except Exception as e:
                latency_ms: float = round((time.time() - start_time) * 1000, 2)
                logger.error(f"ERROR Health check failed: error={e}, latency={latency_ms}ms")

                raise HTTPException(
                    status_code=500,
                    detail={
                        "status": "fail",
                        "error": str(e),
                        "latency_ms": latency_ms,
                    }
                )

    @staticmethod
    def check_database() -> Dict[str, Any]:
        """Check database connectivity."""
        logger.info("HEALTH CHECK: Checking Supabase connectivity for healthcheck")
        return supabase.table("articles").select("id").limit(1).execute()

    @staticmethod
    def interpret_db_status(response: Dict[str, Any]) -> str:
        """Interpret database response status."""
        if response.data is None:
            return "no response"
        elif len(response.data) == 0:
            return "no data"
        return "ok"


