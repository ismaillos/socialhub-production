from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base
import datetime

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    account_id = Column(String)
    username = Column(String)
    profile_pic = Column(String)
    business_id = Column(String, nullable=True)
    access_token = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    account_id = Column(String)
    message = Column(String)
    media_url = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
