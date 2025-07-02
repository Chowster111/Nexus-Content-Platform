from fastapi import APIRouter, HTTPException
from db.supabase_client import supabase
from logging_config import logger
import time

class HealthController:
    def __init__(self):
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self):
        @self.router.get("/health")
        def health_check():
            start_time = time.time()
            try:
                response = self.check_database()
                latency_ms = round((time.time() - start_time) * 1000, 2)

                db_status = self.interpret_db_status(response)
                logger.info(f"HEALTH CHECK: status=ok, db_status={db_status}, latency={latency_ms}ms")

                return {
                    "status": "ok" if db_status == "ok" else "degraded",
                    "database": db_status,
                    "latency_ms": latency_ms,
                }

            except Exception as e:
                latency_ms = round((time.time() - start_time) * 1000, 2)
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
    def check_database():
        logger.info("HEALTH CHECK: Checking Supabase connectivity for healthcheck")
        return supabase.table("articles").select("id").limit(1).execute()

    @staticmethod
    def interpret_db_status(response):
        if response.data is None:
            return "no response"
        elif len(response.data) == 0:
            return "no data"
        return "ok"
