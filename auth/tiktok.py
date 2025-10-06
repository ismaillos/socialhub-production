import os, requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from db.database import SessionLocal
from db.models import Token

router = APIRouter(prefix="/auth/tiktok", tags=["TikTok"])

CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY", "")
CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("TIKTOK_REDIRECT_URI", "https://socialhub-production-production.up.railway.app/auth/tiktok/callback")
SCOPE = "user.info.basic,video.upload"
STATE = "secure_state_12345"

@router.get("/login")
def tiktok_login():
    url = (
        "https://www.tiktok.com/v2/auth/authorize/"
        f"?client_key={CLIENT_KEY}&scope={SCOPE}&response_type=code"
        f"&redirect_uri={REDIRECT_URI}&state={STATE}"
    )
    return RedirectResponse(url=url)

@router.get("/callback")
def tiktok_callback(code: str = None, state: str = None, error: str = None):
    if error:
        return JSONResponse({"status":"error","message":error}, status_code=400)

    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    res = requests.post("https://open-api.tiktok.com/oauth/access_token/", data=data).json()
    if res.get("data") and res["data"].get("access_token"):
        at = res["data"]["access_token"]
        rt = res["data"].get("refresh_token")
    else:
        return JSONResponse({"status":"error","details": res}, status_code=400)

    # Get user info
    headers = {"Authorization": f"Bearer {at}"}
    me = requests.get("https://open-api.tiktok.com/user/info/", headers=headers).json()
    # TikTok returns open_id inside tokens sometimes; fallback:
    open_id = res["data"].get("open_id") if res.get("data") else None
    username = None
    if me.get("data") and me["data"].get("user"):
        username = me["data"]["user"].get("display_name")

    from db.database import SessionLocal
    from db.models import Token
    with SessionLocal() as session:
        existing = session.query(Token).filter(Token.platform=="tiktok").first()
        if not existing: existing = Token(platform="tiktok")
        existing.account_id = open_id or "unknown"
        existing.username = username
        existing.access_token = at
        existing.refresh_token = rt
        session.add(existing)
        session.commit()

    return RedirectResponse(url="/accounts")
