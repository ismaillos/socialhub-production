import requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from db.database import SessionLocal
from db.models import Token
from core.config import get_secret

router = APIRouter(prefix="/auth/youtube", tags=["YouTube"])

CLIENT_ID = get_secret("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = get_secret("GOOGLE_CLIENT_SECRET", "")
REDIRECT_URI = get_secret("GOOGLE_REDIRECT_URI", "")
SCOPE = "https://www.googleapis.com/auth/youtube.readonly openid email"

@router.get("/login")
def yt_login():
    auth_url = ("https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&response_type=code&access_type=offline&prompt=consent"
        f"&scope={SCOPE}")
    return RedirectResponse(url=auth_url)

@router.get("/callback")
def yt_callback(code: str = None, error: str = None):
    if error:
        return JSONResponse({"status":"error","message":error}, status_code=400)
    data = {"code": code,"client_id": CLIENT_ID,"client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,"grant_type": "authorization_code"}
    token_res = requests.post("https://oauth2.googleapis.com/token", data=data).json()
    access_token = token_res.get("access_token"); refresh_token = token_res.get("refresh_token")
    if not access_token:
        return JSONResponse({"status":"error","details": token_res}, status_code=400)
    ch = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
                       headers={"Authorization": f"Bearer {access_token}"}).json()
    channel_id = None; channel_title = None
    if ch.get("items"):
        channel_id = ch["items"][0]["id"]; channel_title = ch["items"][0]["snippet"]["title"]
    with SessionLocal() as s:
        existing = s.query(Token).filter(Token.platform=="youtube", Token.account_id==channel_id).first()
        if existing:
            existing.username = channel_title; existing.access_token = access_token; existing.refresh_token = refresh_token
        else:
            s.add(Token(platform="youtube", account_id=channel_id or "unknown", username=channel_title,
                        access_token=access_token, refresh_token=refresh_token))
        s.commit()
    return RedirectResponse(url="/accounts")
