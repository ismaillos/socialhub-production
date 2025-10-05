from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
import os, urllib.parse, requests
from db.database import SessionLocal
from db.models import Token

router = APIRouter(prefix="/auth/facebook", tags=["Facebook"])

CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("FACEBOOK_REDIRECT_URI", "https://your-domain/auth/facebook/callback")

AUTH_URL = "https://www.facebook.com/v19.0/dialog/oauth"
TOKEN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"
SCOPE = "public_profile,pages_show_list,pages_manage_posts,instagram_basic,instagram_content_publish"

@router.get("/login")
def fb_login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "state": "fb_state_123",
    }
    return RedirectResponse(f"{AUTH_URL}?{urllib.parse.urlencode(params)}")

@router.get("/callback")
def fb_callback(code: str = None, error: str = None, state: str = None):
    if error or not code:
        return JSONResponse({"status":"error","platform":"facebook","message": error or "missing code"}, status_code=400)

    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    token_res = requests.get(TOKEN_URL, params=params).json()
    if "access_token" not in token_res:
        return JSONResponse({"status":"error","platform":"facebook","details": token_res}, status_code=400)

    access_token = token_res["access_token"]

    # Optional: fetch user profile
    me = requests.get("https://graph.facebook.com/me", params={"access_token": access_token}).json()
    account_id = me.get("id", "unknown")
    username = me.get("name", "Facebook User")

    with SessionLocal() as s:
        existing = s.query(Token).filter(Token.platform=="facebook").first()
        if existing:
            existing.account_id = account_id
            existing.username = username
            existing.access_token = access_token
        else:
            s.add(Token(platform="facebook", account_id=account_id, username=username, access_token=access_token))
        s.commit()

    return RedirectResponse(url="/accounts", status_code=302)
