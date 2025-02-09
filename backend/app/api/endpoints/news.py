from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.news import NewsResponse
from app.services.scraper import NBAScraper
from app.db.session import get_db
from app.models.news import News
from fastapi import WebSocket
from app.core.websocket import manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast({"message": "New news available"})
    except Exception:
        await manager.disconnect(websocket)

@router.get("/featured", response_model=List[NewsResponse])
async def get_featured_news(db: Session = Depends(get_db)):
    try:
        scraper = NBAScraper()
        news_items = await scraper.fetch_featured_news()
        
        # Save to database
        for item in news_items:
            db_news = News(
                title=item['title'],
                url=item['url'],
                image_url=item['image_url'],
                content=item['content'],
                published_time=item['published_time']
            )
            db.add(db_news)
        
        db.commit()
        return news_items
    except Exception as e:
        logger.error(f"Error in get_featured_news: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{news_id}", response_model=NewsResponse)
async def get_news_detail(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news


@router.get("/{url:path}")
async def get_news_detail(url: str):
    scraper = NBAScraper()
    return await scraper.fetch_article_detail(url)