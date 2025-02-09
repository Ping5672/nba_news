from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
import pytest
from unittest.mock import patch, AsyncMock
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_featured_news():
    with patch('app.services.scraper.NBAScraper.fetch_featured_news') as mock_fetch:
        mock_fetch.return_value = [
            {
                'title': 'Test News',
                'url': 'test-url',
                'image_url': 'test-image.jpg',
                'content': 'Test content',
                'published_time': '1 hour ago'
            }
        ]
        response = client.get("/api/news/featured")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]['title'] == 'Test News'

def test_get_news_detail():
    async def mock_fetch_article():
        return {
            'content': 'Test content',
            'tags': ['Tag1', 'Tag2']
        }

    with patch('app.services.scraper.NBAScraper.fetch_article_detail', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = {
            'content': 'Test content',
            'tags': ['Tag1', 'Tag2']
        }
        with TestClient(app) as client:
            # Use proper URL encoding
            response = client.get("/api/news/https%3A%2F%2Ftw-nba.udn.com%2Fnba%2Fstory%2F1")
            assert response.status_code == 200
            data = response.json()
            assert data['content'] == 'Test content'