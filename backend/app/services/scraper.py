import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class NBAScraper:
    BASE_URL = "https://tw-nba.udn.com/nba/index"
    
    
    async def fetch_featured_news(self) -> List[Dict]:
        try:
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, headers=headers) as response:
                    html = await response.text()
                
            soup = BeautifulSoup(html, 'html.parser')
            news_items = []
        
            for article in soup.find_all('dt'):
                try:
                    link = article.find('a')
                    if not link:
                        continue
                
                    title = link.find('h3')
                    image = link.find('img')
                    content = link.find('p')
                    published = link.find('b', class_='h24')
                
                    if all([title, image, content, published]):
                        news_items.append({
                        'title': title.text.strip(),
                        'url': link['href'],
                        'image_url': image['src'],
                        'content': content.text.strip(),
                        'published_time': published.text.strip()
                        })
                    
                except Exception as e:
                    logger.error(f"Error processing article: {str(e)}")
                    continue
                
            return news_items
            
        except Exception as e:
            logger.error(f"Error scraping news: {str(e)}")
            raise
    
    
            
    
    async def fetch_article_detail(self, url: str) -> Dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
    
        soup = BeautifulSoup(html, 'html.parser')
        content = ''
        for p in soup.find_all('p'):
            content += p.text.strip() + '\n'
    
        return {
        'content': content,
        'tags': [a.text for a in soup.find_all('a', class_='tag_a')]
        }