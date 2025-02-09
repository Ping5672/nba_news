
import pytest
import asyncio
import aiohttp
import time
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

async def make_request(session, url):
    async with session.get(url) as response:
        return response.status

async def load_test(url, total_requests, concurrent_requests):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(total_requests):
            tasks.append(make_request(session, url))
            if len(tasks) >= concurrent_requests:
                await asyncio.gather(*tasks)
                tasks = []
        if tasks:
            await asyncio.gather(*tasks)

@pytest.mark.asyncio
async def test_api_load():
    # Start the application first
    url = "http://localhost:8000/api/news/featured"
    with TestClient(app) as client:
        response = client.get("/api/news/featured")
        assert response.status_code == 200