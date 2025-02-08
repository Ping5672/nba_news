# backend/app/core/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.scraper import NBAScraper

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('interval', minutes=30)
async def scheduled_scraping():
    scraper = NBAScraper()
    await scraper.fetch_featured_news()

def start_scheduler():
    scheduler.start()