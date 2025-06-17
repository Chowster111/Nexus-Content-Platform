from fastapi import APIRouter
from scraper.netflix import scrape_all_netflix_articles
from scraper.airbnb import scrape_all_airbnb_articles
from scraper.stripe import scrape_all_stripe_articles
from scraper.tinder import scrape_all_tinder_articles
from scraper.uber import scrape_all_uber_articles
from .utils.trigger_scrape import trigger_scrape


router = APIRouter()

@router.post("/netflix")
def trigger_scrape_netflix():
    return trigger_scrape("Netflix Tech Blog", scrape_all_netflix_articles)

@router.post("/airbnb")
def trigger_scrape_airbnb():
    return trigger_scrape("Airbnb Engineering Blog", scrape_all_airbnb_articles)

@router.post("/stripe")
def trigger_scrape_stripe():
    return trigger_scrape("Stripe Blog", scrape_all_stripe_articles)

@router.post("/tinder")
def trigger_scrape_tinder():
    return trigger_scrape("Tinder Tech Blog", scrape_all_tinder_articles)


@router.post("/uber")
def trigger_scrape_uber():
    return trigger_scrape("Uber Engineering Blog", scrape_all_uber_articles)


@router.post("/all")
def trigger_scrape_all():
    results = {}
    results["Netflix"] = trigger_scrape("Netflix Tech Blog", scrape_all_netflix_articles)
    results["Airbnb"] = trigger_scrape("Airbnb Engineering Blog", scrape_all_airbnb_articles)
    results["Stripe"] = trigger_scrape("Stripe Blog", scrape_all_stripe_articles)
    results["Tinder"] = trigger_scrape("Tinder Tech Blog", scrape_all_tinder_articles)
    results["Uber"] = trigger_scrape("Uber Engineering Blog", scrape_all_uber_articles)
    return results
