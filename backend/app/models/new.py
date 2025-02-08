from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.sql import func
from app.db.base import Base

class News(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String(255), unique=True, nullable=False)
    image_url = Column(String(255))
    published_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Create indexes for frequent queries
    __table_args__ = (
        Index('idx_published_at', published_at.desc()),
        Index('idx_title', title),
    )