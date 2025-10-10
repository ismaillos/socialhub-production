
from authlib.integrations.starlette_client import OAuth
from fastapi import Request
import os

oauth = OAuth()
oauth.register(
    name='facebook',
    client_id=os.getenv("FB_CLIENT_ID"),
    client_secret=os.getenv("FB_CLIENT_SECRET"),
    access_token_url='https://graph.facebook.com/v18.0/oauth/access_token',
    authorize_url='https://www.facebook.com/v18.0/dialog/oauth',
    api_base_url='https://graph.facebook.com/v18.0/',
    client_kwargs={'scope': 'pages_manage_posts,pages_read_engagement,publish_video'}
)

async def facebook_login(request: Request):
    redirect_uri = 'http://localhost:8000/auth/facebook/callback'
    return await oauth.facebook.authorize_redirect(request, redirect_uri)

async def facebook_callback(request: Request):
    token = await oauth.facebook.authorize_access_token(request)
    user_info = await oauth.facebook.get('me', token=token)
    return token, user_info.json()
