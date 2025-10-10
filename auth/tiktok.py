
from fastapi import Request
from authlib.integrations.starlette_client import OAuth
from sqlmodel import Session, select
from config import settings
from models.user_settings import UserSettings
from utils.encryption import encrypt_value
import os

oauth = OAuth()
oauth.register(
    name='tiktok',
    client_id=os.getenv("TIKTOK_CLIENT_ID"),
    client_secret=os.getenv("TIKTOK_CLIENT_SECRET"),
    access_token_url='https://open.tiktokapis.com/v2/oauth/token/',
    authorize_url='https://www.tiktok.com/v2/auth/authorize/',
    api_base_url='https://open.tiktokapis.com/v2/',
    client_kwargs={'scope': 'user.info.basic video.upload', 'token_endpoint_auth_method': 'client_secret_post'}
)

async def tiktok_login(request: Request):
    redirect_uri = os.getenv("BASE_URL", "http://localhost:8080") + "/auth/tiktok/callback"
    return await oauth.tiktok.authorize_redirect(request, redirect_uri)

async def tiktok_callback(request: Request):
    token = await oauth.tiktok.authorize_access_token(request)
    user = await oauth.tiktok.get('user/info/', token=token)
    user_id = user.json().get("data", {}).get("user", {}).get("open_id", "unknown")

    with Session(settings.engine) as session:
        existing = session.exec(select(UserSettings).where(UserSettings.user_id == user_id)).first()
        if not existing:
            new_user = UserSettings(user_id=user_id, tiktok_token=encrypt_value(token['access_token']))
            session.add(new_user)
        else:
            existing.tiktok_token = encrypt_value(token['access_token'])
            session.add(existing)
        session.commit()

    return {"message": "TikTok connected", "user_id": user_id}
