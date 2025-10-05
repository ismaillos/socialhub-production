from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
import os, urllib.parse, requests
from db.database import SessionLocal
from db.models import Token

router = APIRouter(prefix="/auth/tiktok", tags=["TikTok"])

CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY", "")
CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("TIKTOK_REDIRECT_URI", "https://your-domain/auth/tiktok/callback")

# TikTok OAuth v2
AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
TOKEN_URL = "https://open-api.tiktok.com/oauth/access_token/"
SCOPE = "user.info.basic,video.upload"

@router.get("/login")
def tiktok_login():
    params = {
        "client_key": CLIENT_KEY,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "state": "tt_state_123",
    }
    return RedirectResponse(f"{AUTH_URL}?{urllib.parse.urlencode(params)}")

@router.get("/callback")
def tiktok_callback(code: str = None, error: str = None, state: str = None):
    if error or not code:
        return JSONResponse({"status":"error","platform":"tiktok","message": error or "missing code"}, status_code=400)

    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    token_res = requests.post(TOKEN_URL, data=data).json()
    if "access_token" not in token_res.get("data", {}):
        return JSONResponse({"status":"error","platform":"tiktok","details": token_res}, status_code=400)

    access_token = token_res["data"]["access_token"]

    # Optional: fetch user
    user = requests.get(
        "https://open-api.tiktok.com/user/info/",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()
    account_id = (user.get("data") or {}).get("user_id", "unknown")
    username = ((user.get("data") or {}).get("user") or {}).get("display_name", "TikTok User")

    with SessionLocal() as s:
        existing = s.query(Token).filter(Token.platform=="tiktok").first()
        if existing:
            existing.account_id = account_id
            existing.username = username
            existing.access_token = access_token
        else:
            s.add(Token(platform="tiktok", account_id=account_id, username=username, access_token=access_token))
        s.commit()

    return RedirectResponse(url="/accounts", status_code=302)
