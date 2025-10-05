from sqlalchemy import Column, Integer, String, Text, DateTime
from db.database import Base
import datetime

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)
    account_id = Column(String)
    account_name = Column(String)
    access_token = Column(Text)
    expires_at = Column(DateTime, default=datetime.datetime.utcnow)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    account_id = Column(String)
    message = Column(Text)
    media_url = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
