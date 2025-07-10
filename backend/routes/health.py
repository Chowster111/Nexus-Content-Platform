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
        @self.router.get("/health")
        def health_check() -> Dict[str, Any]:
            """Perform a comprehensive health check."""
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


