from sqlalchemy import Column, Integer, String, DateTime, Text
from db.database import Base
import datetime

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)                # facebook, instagram, tiktok, youtube
    account_id = Column(String)                           # user id / page id / channel id / open_id
    username = Column(String, nullable=True)
    profile_pic = Column(String, nullable=True)
    business_id = Column(String, nullable=True)           # ig_business_id or page_id when relevant
    page_id = Column(String, nullable=True)               # facebook page id (if applicable)
    page_access_token = Column(Text, nullable=True)       # page token for FB/IG publishing
    access_token = Column(Text)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)          # when the token expires
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    account_id = Column(String)
    message = Column(Text)
    media_url = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
