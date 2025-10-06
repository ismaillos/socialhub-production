from sqlalchemy import Column, Integer, String, DateTime, Text
from db.database import Base
import datetime
class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)
    account_id = Column(String)
    username = Column(String, nullable=True)
    profile_pic = Column(String, nullable=True)
    business_id = Column(String, nullable=True)
    page_id = Column(String, nullable=True)
    page_access_token = Column(Text, nullable=True)
    access_token = Column(Text)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    account_id = Column(String)
    message = Column(Text)
    media_url = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
