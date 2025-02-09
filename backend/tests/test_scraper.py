import pytest
from app.services.scraper import NBAScraper
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
class TestNBAScraper:
    async def test_fetch_featured_news_success(self):
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.text.return_value = """
                <dt>
                    <a href="test-url">
                        <h3>Test Title</h3>
                        <img src="test-image.jpg">
                        <p>Test content</p>
                        <b class="h24">1 hour ago</b>
                    </a>
                </dt>
            """
            mock_get.return_value.__aenter__.return_value = mock_response
            
            scraper = NBAScraper()
            result = await scraper.fetch_featured_news()
            
            assert result[0]['title'] == 'Test Title'
            assert result[0]['url'] == 'test-url'

    async def test_fetch_article_detail_success(self):
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.text.return_value = """
                <p>Test content</p>
                <a class="tag_a">Test Tag</a>
            """
            mock_get.return_value.__aenter__.return_value = mock_response
            
            scraper = NBAScraper()
            result = await scraper.fetch_article_detail('test-url')
            
            assert 'Test content' in result['content']
            assert 'Test Tag' in result['tags']