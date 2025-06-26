# routes/health.py
from fastapi import APIRouter, HTTPException
from db.supabase_client import supabase
import time

router = APIRouter()

@router.get("/health")
def health_check():
    try:
        start_time = time.time()
        response = supabase.table("articles").select("id").limit(1).execute()
        db_status = "ok" if response.data else "no data"
        latency_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "status": "ok",
            "database": db_status,
            "latency_ms": latency_ms,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "fail",
            "error": str(e)
        })
