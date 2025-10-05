from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
import os, urllib.parse, requests
from db.database import SessionLocal
from db.models import Token

router = APIRouter(prefix="/auth/youtube", tags=["YouTube / Google"])

CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("YOUTUBE_REDIRECT_URI", "https://your-domain/auth/youtube/callback")

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPE = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly"

@router.get("/login")
def yt_login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent",
        "state": "yt_state_123",
    }
    return RedirectResponse(f"{AUTH_URL}?{urllib.parse.urlencode(params)}")

@router.get("/callback")
def yt_callback(code: str = None, error: str = None, state: str = None):
    if error or not code:
        return JSONResponse({"status":"error","platform":"youtube","message": error or "missing code"}, status_code=400)

    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_res = requests.post(TOKEN_URL, data=data).json()
    if "access_token" not in token_res:
        return JSONResponse({"status":"error","platform":"youtube","details": token_res}, status_code=400)

    access_token = token_res["access_token"]
    refresh_token = token_res.get("refresh_token")

    # Optional: get channel info
    ch = requests.get(
        "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()
    account_id = (ch.get("items") or [{}])[0].get("id", "unknown")
    username = ((ch.get("items") or [{}])[0].get("snippet") or {}).get("title", "YouTube User")

    # Save
    with SessionLocal() as s:
        existing = s.query(Token).filter(Token.platform=="youtube").first()
        if existing:
            existing.account_id = account_id
            existing.username = username
            existing.access_token = access_token
        else:
            s.add(Token(platform="youtube", account_id=account_id, username=username, access_token=access_token))
        s.commit()

    return RedirectResponse(url="/accounts", status_code=302)
