from pydantic import BaseModel
from datetime import datetime

class NewsResponse(BaseModel):
    title: str
    url: str
    image_url: str | None
    content: str
    published_time: str | None