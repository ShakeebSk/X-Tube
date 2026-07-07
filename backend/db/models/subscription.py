from db.base import Base
from sqlalchemy import Column, String, ForeignKey

class Subscription(Base):
    __tablename__ = "subscriptions"

    subscriber_id = Column(String, ForeignKey("users.cognito_sub"), primary_key=True)
    channel_id = Column(String, ForeignKey("users.cognito_sub"), primary_key=True)
