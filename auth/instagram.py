import requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from db.database import SessionLocal
from db.models import Token
from core.config import get_secret

router = APIRouter(prefix="/auth/instagram", tags=["Instagram"])

CLIENT_ID = get_secret("FACEBOOK_CLIENT_ID", "")
CLIENT_SECRET = get_secret("FACEBOOK_CLIENT_SECRET", "")
REDIRECT_URI = get_secret("INSTAGRAM_REDIRECT_URI", "")
SCOPE = "instagram_basic,instagram_content_publish,pages_show_list,business_management"

@router.get("/login")
def ig_login():
    url = ("https://www.facebook.com/v19.0/dialog/oauth"
           f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
           f"&scope={SCOPE}&response_type=code")
    return RedirectResponse(url=url)

@router.get("/callback")
def ig_callback(code: str = None, error: str = None):
    if error:
        return JSONResponse({"status":"error","message":error}, status_code=400)
    token_res = requests.get("https://graph.facebook.com/v19.0/oauth/access_token",
                             params={"client_id": CLIENT_ID, "redirect_uri": REDIRECT_URI,
                                     "client_secret": CLIENT_SECRET, "code": code}).json()
    user_access_token = token_res.get("access_token")
    if not user_access_token:
        return JSONResponse({"status":"error","details": token_res}, status_code=400)
    pages = requests.get("https://graph.facebook.com/me/accounts",
                         params={"access_token": user_access_token}).json().get("data", [])
    with SessionLocal() as s:
        for p in pages:
            pid = p["id"]
            detail = requests.get(f"https://graph.facebook.com/{pid}",
                                  params={"fields":"instagram_business_account,access_token,name",
                                          "access_token": user_access_token}).json()
            ig_obj = detail.get("instagram_business_account")
            page_token = detail.get("access_token") or p.get("access_token")
            page_name = detail.get("name") or pid
            if not ig_obj or not ig_obj.get("id"):
                continue
            ig_id = ig_obj["id"]
            ig_profile = requests.get(f"https://graph.facebook.com/{ig_id}",
                                      params={"fields":"username,profile_picture_url",
                                              "access_token": page_token}).json()
            ig_username = ig_profile.get("username")
            profile_pic = ig_profile.get("profile_picture_url")
            existing = s.query(Token).filter(Token.platform=="instagram", Token.account_id==ig_id).first()
            if existing:
                existing.username = ig_username; existing.profile_pic = profile_pic
                existing.business_id = ig_id; existing.page_id = pid
                existing.page_access_token = page_token; existing.access_token = user_access_token
            else:
                s.add(Token(platform="instagram", account_id=ig_id, username=ig_username, profile_pic=profile_pic,
                            business_id=ig_id, page_id=pid, page_access_token=page_token, access_token=user_access_token))
        s.commit()
    return RedirectResponse(url="/accounts")
