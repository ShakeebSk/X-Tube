from sqlalchemy import Column, String, Integer, ForeignKey
from db.base import Base

class Download(Base):
    __tablename__ = "downloads"

    user_id = Column(String, ForeignKey("users.cognito_sub"), primary_key=True)
    video_id = Column(String, ForeignKey("videos.id"), primary_key=True)
    count = Column(Integer, default=1)
