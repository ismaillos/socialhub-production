from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
import os, urllib.parse, requests
from db.database import SessionLocal
from db.models import Token

router = APIRouter(prefix="/auth/instagram", tags=["Instagram"])

CLIENT_ID = os.getenv("INSTAGRAM_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("INSTAGRAM_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("INSTAGRAM_REDIRECT_URI", "https://your-domain/auth/instagram/callback")

AUTH_URL = "https://api.instagram.com/oauth/authorize"
TOKEN_URL = "https://api.instagram.com/oauth/access_token"
SCOPE = "user_profile,user_media"

@router.get("/login")
def ig_login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "response_type": "code",
        "state": "ig_state_123",
    }
    return RedirectResponse(f"{AUTH_URL}?{urllib.parse.urlencode(params)}")

@router.get("/callback")
def ig_callback(code: str = None, error: str = None, state: str = None):
    if error or not code:
        return JSONResponse({"status":"error","platform":"instagram","message": error or "missing code"}, status_code=400)

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    token_res = requests.post(TOKEN_URL, data=data).json()
    if "access_token" not in token_res:
        return JSONResponse({"status":"error","platform":"instagram","details": token_res}, status_code=400)

    access_token = token_res["access_token"]
    user = requests.get(
        f"https://graph.instagram.com/me?fields=id,username&access_token={access_token}"
    ).json()
    account_id = user.get("id", "unknown")
    username = user.get("username", "Instagram User")

    with SessionLocal() as s:
        existing = s.query(Token).filter(Token.platform=="instagram").first()
        if existing:
            existing.account_id = account_id
            existing.username = username
            existing.access_token = access_token
        else:
            s.add(Token(platform="instagram", account_id=account_id, username=username, access_token=access_token))
        s.commit()

    return RedirectResponse(url="/accounts", status_code=302)
