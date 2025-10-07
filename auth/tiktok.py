import requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from db.database import SessionLocal
from db.models import Token
from core.config import get_secret

router = APIRouter(prefix="/auth/tiktok", tags=["TikTok"])

CLIENT_KEY = get_secret("TIKTOK_CLIENT_KEY", "")
CLIENT_SECRET = get_secret("TIKTOK_CLIENT_SECRET", "")
REDIRECT_URI = get_secret("TIKTOK_REDIRECT_URI", "")
SCOPE = "user.info.basic,video.upload"
STATE = "secure_state_12345"

@router.get("/login")
def tiktok_login():
    url = ("https://www.tiktok.com/v2/auth/authorize/"
           f"?client_key={CLIENT_KEY}&scope={SCOPE}&response_type=code"
           f"&redirect_uri={REDIRECT_URI}&state={STATE}")
    return RedirectResponse(url=url)

@router.get("/callback")
def tiktok_callback(code: str = None, state: str = None, error: str = None):
    if error:
        return JSONResponse({"status":"error","message":error}, status_code=400)
    data = {"client_key": CLIENT_KEY,"client_secret": CLIENT_SECRET,"code": code,
            "grant_type": "authorization_code","redirect_uri": REDIRECT_URI}
    res = requests.post("https://open-api.tiktok.com/oauth/access_token/", data=data).json()
    if res.get("data") and res["data"].get("access_token"):
        at = res["data"]["access_token"]; rt = res["data"].get("refresh_token")
    else:
        return JSONResponse({"status":"error","details": res}, status_code=400)
    headers = {"Authorization": f"Bearer {at}"}
    me = requests.get("https://open-api.tiktok.com/user/info/", headers=headers).json()
    open_id = res["data"].get("open_id") if res.get("data") else None
    username = None
    if me.get("data") and me["data"].get("user"):
        username = me["data"]["user"].get("display_name")
    with SessionLocal() as s:
        existing = s.query(Token).filter(Token.platform=="tiktok", Token.account_id==open_id).first()
        if existing:
            existing.username = username; existing.access_token = at; existing.refresh_token = rt
        else:
            s.add(Token(platform="tiktok", account_id=open_id or "unknown", username=username,
                        access_token=at, refresh_token=rt))
        s.commit()
    return RedirectResponse(url="/accounts")
