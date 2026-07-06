from sqlalchemy import Column, String, Boolean, ForeignKey
from db.base import Base

class LikeDislike(Base):
    __tablename__ = "like_dislike"

    user_id = Column(String, ForeignKey("users.cognito_sub"), primary_key=True)
    video_id = Column(String, ForeignKey("videos.id"), primary_key=True)
    is_like = Column(Boolean, nullable=False)  # True = like, False = dislike
