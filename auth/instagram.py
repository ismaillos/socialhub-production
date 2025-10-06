import os, requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from db.database import SessionLocal
from db.models import Token

router = APIRouter(prefix="/auth/instagram", tags=["Instagram"])

# Instagram uses the same Meta app (client id/secret) but a different redirect URI
CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("INSTAGRAM_REDIRECT_URI", "https://socialhub-production-production.up.railway.app/auth/instagram/callback")
SCOPE = "instagram_basic,instagram_content_publish,pages_show_list,business_management"

@router.get("/login")
def ig_login():
    auth_url = (
        "https://www.facebook.com/v19.0/dialog/oauth"
        f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE}&response_type=code"
    )
    return RedirectResponse(url=auth_url)

@router.get("/callback")
def ig_callback(code: str = None, error: str = None):
    if error:
        return JSONResponse({"status":"error","message":error}, status_code=400)

    token_res = requests.get(
        "https://graph.facebook.com/v19.0/oauth/access_token",
        params={
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "client_secret": CLIENT_SECRET,
            "code": code
        }
    ).json()
    access_token = token_res.get("access_token")
    if not access_token:
        return JSONResponse({"status":"error","details": token_res}, status_code=400)

    # Find connected Instagram Business Account from Pages
    pages = requests.get("https://graph.facebook.com/me/accounts", params={"access_token": access_token}).json()
    ig_business_id = None
    page_id = None
    page_token = None
    if "data" in pages:
        for p in pages["data"]:
            pid = p["id"]
            details = requests.get(
                f"https://graph.facebook.com/{pid}",
                params={"fields":"instagram_business_account,access_token", "access_token": access_token}
            ).json()
            ig_obj = details.get("instagram_business_account")
            if ig_obj and ig_obj.get("id"):
                ig_business_id = ig_obj["id"]
                page_id = pid
                page_token = details.get("access_token", p.get("access_token"))
                break

    # Fetch IG username
    ig_username = None
    if ig_business_id and page_token:
        ig_profile = requests.get(
            f"https://graph.facebook.com/{ig_business_id}",
            params={"fields":"username,profile_picture_url", "access_token": page_token}
        ).json()
        ig_username = ig_profile.get("username")
        profile_pic = ig_profile.get("profile_picture_url")
    else:
        profile_pic = None

    with SessionLocal() as session:
        existing = session.query(Token).filter(Token.platform=="instagram").first()
        if not existing:
            existing = Token(platform="instagram")
        existing.account_id = ig_business_id or "unknown"
        existing.username = ig_username
        existing.business_id = ig_business_id
        existing.page_id = page_id
        existing.page_access_token = page_token
        existing.access_token = access_token  # user token; IG publishing uses page token
        existing.profile_pic = profile_pic
        session.add(existing)
        session.commit()

    return RedirectResponse(url="/accounts")
