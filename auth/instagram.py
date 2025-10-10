
from fastapi import Request
from authlib.integrations.starlette_client import OAuth
from sqlmodel import Session, select
from config import settings
from models.user_settings import UserSettings
from utils.encryption import encrypt_value
import os

oauth = OAuth()
oauth.register(
    name='instagram',
    client_id=os.getenv("FB_CLIENT_ID"),
    client_secret=os.getenv("FB_CLIENT_SECRET"),
    access_token_url='https://graph.facebook.com/v18.0/oauth/access_token',
    authorize_url='https://www.facebook.com/v18.0/dialog/oauth',
    api_base_url='https://graph.facebook.com/v18.0/',
    client_kwargs={'scope': 'instagram_basic,pages_show_list'}
)

async def instagram_login(request: Request):
    redirect_uri = os.getenv("BASE_URL", "http://localhost:8080") + "/auth/instagram/callback"
    return await oauth.instagram.authorize_redirect(request, redirect_uri)

async def instagram_callback(request: Request):
    token = await oauth.instagram.authorize_access_token(request)
    user = await oauth.instagram.get('me', token=token)
    user_id = str(user.json().get("id"))

    with Session(settings.engine) as session:
        existing = session.exec(select(UserSettings).where(UserSettings.user_id == user_id)).first()
        if not existing:
            new_user = UserSettings(user_id=user_id, instagram_token=encrypt_value(token['access_token']))
            session.add(new_user)
        else:
            existing.instagram_token = encrypt_value(token['access_token'])
            session.add(existing)
        session.commit()

    return {"message": "Instagram connected", "user_id": user_id}
