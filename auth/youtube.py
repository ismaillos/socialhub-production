
from fastapi import Request
from authlib.integrations.starlette_client import OAuth
from sqlmodel import Session, select
from config import settings
from models.user_settings import UserSettings
from utils.encryption import encrypt_value
import os

oauth = OAuth()
oauth.register(
    name='youtube',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'https://www.googleapis.com/auth/youtube.upload', 'access_type': 'offline'}
)

async def youtube_login(request: Request):
    redirect_uri = os.getenv("BASE_URL", "http://localhost:8080") + "/auth/youtube/callback"
    return await oauth.youtube.authorize_redirect(request, redirect_uri)

async def youtube_callback(request: Request):
    token = await oauth.youtube.authorize_access_token(request)
    user = await oauth.youtube.get('userinfo', token=token)
    user_id = str(user.json().get("id"))

    with Session(settings.engine) as session:
        existing = session.exec(select(UserSettings).where(UserSettings.user_id == user_id)).first()
        if not existing:
            new_user = UserSettings(user_id=user_id, youtube_token=encrypt_value(token['access_token']))
            session.add(new_user)
        else:
            existing.youtube_token = encrypt_value(token['access_token'])
            session.add(existing)
        session.commit()

    return {"message": "YouTube connected", "user_id": user_id}
