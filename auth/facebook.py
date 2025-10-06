import os, requests, datetime
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from db.database import SessionLocal
from db.models import Token

router = APIRouter(prefix="/auth/facebook", tags=["Facebook"])

CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("FACEBOOK_REDIRECT_URI", "https://socialhub-production-production.up.railway.app/auth/facebook/callback")
SCOPE = "pages_show_list,pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish,business_management"

@router.get("/login")
def fb_login():
    auth_url = (
        "https://www.facebook.com/v19.0/dialog/oauth"
        f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE}&response_type=code"
    )
    return RedirectResponse(url=auth_url)

@router.get("/callback")
def fb_callback(code: str = None, error: str = None):
    if error:
        return JSONResponse({"status":"error","message":error}, status_code=400)

    token_params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "client_secret": CLIENT_SECRET,
        "code": code
    }
    token_res = requests.get("https://graph.facebook.com/v19.0/oauth/access_token", params=token_params).json()
    access_token = token_res.get("access_token")
    if not access_token:
        return JSONResponse({"status":"error","details": token_res}, status_code=400)

    # Get user
    me = requests.get("https://graph.facebook.com/me", params={"access_token": access_token, "fields": "id,name"}).json()

    # Get Pages + pick first for demo (you can render selection UI later)
    pages = requests.get("https://graph.facebook.com/me/accounts", params={"access_token": access_token}).json()
    page_id = None
    page_token = None
    if "data" in pages and pages["data"]:
        page_id = pages["data"][0]["id"]
        page_token = pages["data"][0].get("access_token")

    with SessionLocal() as session:
        existing = session.query(Token).filter(Token.platform=="facebook").first()
        if not existing:
            existing = Token(platform="facebook")
        existing.account_id = me.get("id")
        existing.username = me.get("name")
        existing.access_token = access_token
        existing.page_id = page_id
        existing.page_access_token = page_token
        session.add(existing)
        session.commit()

    return RedirectResponse(url="/accounts")
