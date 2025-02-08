import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class NBAScraper:
    BASE_URL = "https://tw-nba.udn.com/nba/index"
    
    async def fetch_featured_news(self) -> List[Dict]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL) as response:
                    html = await response.text()
                
            soup = BeautifulSoup(html, 'html.parser')
            news_items = []
        
            for article in soup.find_all('dt'):
                link = article.find('a')
                if not link:
                    continue
                
            news_items.append({
                'title': link.find('h3').text.strip(),
                'url': link['href'],
                'image_url': link.find('img')['src'],
                'content': link.find('p').text.strip(),
                'published_time': link.find('b', class_='h24').text.strip()
            })
            
            return news_items
            
        except Exception as e:
            logger.error(f"Error scraping news: {str(e)}")
            raise