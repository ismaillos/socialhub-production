
from fastapi import Request
from authlib.integrations.starlette_client import OAuth
from sqlmodel import Session, select
from config import settings
from models.user_settings import UserSettings
from utils.encryption import encrypt_value
import os

oauth = OAuth()
oauth.register(
    name='facebook',
    client_id=os.getenv("FB_CLIENT_ID"),
    client_secret=os.getenv("FB_CLIENT_SECRET"),
    access_token_url='https://graph.facebook.com/v18.0/oauth/access_token',
    authorize_url='https://www.facebook.com/v18.0/dialog/oauth',
    api_base_url='https://graph.facebook.com/v18.0/',
    client_kwargs={'scope': 'pages_show_list,pages_read_engagement,pages_manage_posts,pages_manage_metadata'}
)

async def facebook_login(request: Request):
    redirect_uri = os.getenv("BASE_URL", "http://localhost:8080") + "/auth/facebook/callback"
    return await oauth.facebook.authorize_redirect(request, redirect_uri)

async def facebook_callback(request: Request):
    token = await oauth.facebook.authorize_access_token(request)
    user = await oauth.facebook.get('me', token=token)
    pages = await oauth.facebook.get('me/accounts', token=token)

    user_id = str(user.json().get("id"))
    fb_access_token = token['access_token']

    # Get first page token if available
    page_data = pages.json().get("data", [])
    page_id = page_data[0]["id"] if page_data else None
    page_access_token = page_data[0]["access_token"] if page_data else None

    # Encrypt and store
    with Session(settings.engine) as session:
        existing = session.exec(select(UserSettings).where(UserSettings.user_id == user_id)).first()
        if not existing:
            new_user = UserSettings(
                user_id=user_id,
                facebook_token=encrypt_value(page_access_token or fb_access_token)
            )
            session.add(new_user)
        else:
            existing.facebook_token = encrypt_value(page_access_token or fb_access_token)
            session.add(existing)
        session.commit()

    return {
        "message": "Facebook account connected and token stored",
        "user_id": user_id,
        "page_id": page_id
    }
