# tests/test_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from app.models.news import News
from unittest.mock import patch, AsyncMock
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_full_scraping_flow():
    with patch('app.services.scraper.NBAScraper.fetch_featured_news') as mock_fetch:
        mock_fetch.return_value = [{
            'title': 'Test News',
            'url': 'test-url',
            'image_url': 'test-image.jpg',
            'content': 'Test content',
            'published_time': '1 hour ago'
        }]
        
        with TestClient(app) as client:
            response = client.get("/api/news/featured")
            assert response.status_code == 200
            news_items = response.json()
            assert len(news_items) > 0
            assert news_items[0]['title'] == 'Test News'