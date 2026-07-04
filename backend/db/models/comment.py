from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from datetime import datetime
from db.base import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.cognito_sub"))
    video_id = Column(String, ForeignKey("videos.id"))
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
