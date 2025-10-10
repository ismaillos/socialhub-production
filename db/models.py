from sqlalchemy import Column, Integer, String, DateTime, Text, UniqueConstraint
from db.database import Base
import datetime

class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)
    account_id = Column(String, index=True)
    username = Column(String, nullable=True)
    profile_pic = Column(String, nullable=True)
    business_id = Column(String, nullable=True)  # IG business id
    page_id = Column(String, nullable=True)      # FB page id
    page_access_token = Column(Text, nullable=True)
    access_token = Column(Text)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint('platform','account_id', name='uq_platform_account'),)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    account_id = Column(String)
    message = Column(Text)
    media_url = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class AppSecret(Base):
    __tablename__ = 'app_secrets'
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value_enc = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
