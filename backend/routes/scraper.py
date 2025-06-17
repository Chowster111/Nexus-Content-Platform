from http.client import HTTPException
from fastapi import APIRouter
from .utils.trigger_scrape import trigger_scrape, SCRAPER_MAP

router = APIRouter()

@router.post("/select/{source}")
def trigger_scrape_source(source):
    source = source.lower()
    instanceFn = SCRAPER_MAP.get(source, None)
    if not instanceFn:
        raise HTTPException(status_code=400, detail=f"Invalid source '{source}'. Must be one of {list(SCRAPER_MAP.keys())}")
    return trigger_scrape(source, instanceFn().scrape)



@router.post("/all")
def trigger_scrape_all():
    results = {}
    for source in SCRAPER_MAP:
        try:
            results[source] = trigger_scrape(source, SCRAPER_MAP[source]().scrape)
        except Exception as e:
            results[source] = {"error": str(e)}
    return results
