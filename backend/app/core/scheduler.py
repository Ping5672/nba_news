# backend/app/core/scheduler.py
import asyncio
import logging
from datetime import datetime
from app.services.scraper import NBAScraper

logger = logging.getLogger(__name__)

class NewsScheduler:
    def __init__(self, interval_minutes: int = 30):
        self.interval = interval_minutes * 60
        self.running = False
        self.scraper = None

    async def run_once(self):
        """Run one iteration of the scraping task"""
        if not self.scraper:
            self.scraper = NBAScraper()
        await self.scraper.fetch_featured_news()

    async def start(self):
        self.running = True
        if not self.scraper:
            self.scraper = NBAScraper()
        while self.running:
            await self.run_once()
            await asyncio.sleep(self.interval)

    def stop(self):
        self.running = False
        
scheduler = NewsScheduler()