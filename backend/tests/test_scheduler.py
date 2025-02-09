
import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from app.core.scheduler import NewsScheduler
from unittest.mock import patch, AsyncMock
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import pytest
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_scheduler():
    scheduler = NewsScheduler(interval_minutes=1)

    with patch('app.services.scraper.NBAScraper', new_callable=AsyncMock) as MockScraper:
        mock_instance = AsyncMock()
        mock_instance.fetch_featured_news.return_value = []
        MockScraper.return_value = mock_instance
        
        scheduler.scraper = mock_instance  # Set the mock instance directly
        await scheduler.run_once()
        
        assert mock_instance.fetch_featured_news.called

@pytest.mark.asyncio
async def test_scheduler_error_handling():
    scheduler = NewsScheduler(interval_minutes=1)
    
    with patch('app.services.scraper.NBAScraper') as MockScraper:
        mock_instance = AsyncMock()
        MockScraper.return_value = mock_instance
        mock_instance.fetch_featured_news.side_effect = Exception("Test error")
        
        scheduler_task = asyncio.create_task(scheduler.start())
        await asyncio.sleep(0.1)
        scheduler.stop()
        try:
            await asyncio.wait_for(scheduler_task, timeout=0.5)
        except asyncio.TimeoutError:
            pass  # Expected behavior