# routes/health.py
from fastapi import APIRouter, HTTPException
from db.supabase_client import supabase
from logging_config import logger
import time

router = APIRouter()

@router.get("/health")
def health_check():
    start_time = time.time()

    try:
        response = supabase.table("articles").select("id").limit(1).execute()
        latency_ms = round((time.time() - start_time) * 1000, 2)

        if response.data is None:
            db_status = "no response"
        elif len(response.data) == 0:
            db_status = "no data"
        else:
            db_status = "ok"

        logger.info(f"✅ Health check: status=ok, db_status={db_status}, latency={latency_ms}ms")

        return {
            "status": "ok" if db_status == "ok" else "degraded",
            "database": db_status,
            "latency_ms": latency_ms,
        }

    except Exception as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        logger.error(f"❌ Health check failed: error={e}, latency={latency_ms}ms")

        raise HTTPException(
            status_code=500,
            detail={
                "status": "fail",
                "error": str(e),
                "latency_ms": latency_ms,
            }
        )
