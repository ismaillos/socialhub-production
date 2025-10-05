from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
import requests, os
from auth.oauth_utils import save_token, success_redirect

router = APIRouter(prefix="/auth/instagram", tags=["Instagram"])

INSTAGRAM_CLIENT_ID = os.getenv("INSTAGRAM_CLIENT_ID")
INSTAGRAM_CLIENT_SECRET = os.getenv("INSTAGRAM_CLIENT_SECRET")
REDIRECT_URI = os.getenv("INSTAGRAM_REDIRECT_URI", "https://socialhub-production-production.up.railway.app/auth/instagram/callback")

@router.get("/login")
def instagram_login():
    scope = "user_profile,user_media"
    auth_url = (
        "https://api.instagram.com/oauth/authorize"
        f"?client_id={INSTAGRAM_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={scope}"
        "&response_type=code"
    )
    return RedirectResponse(url=auth_url)

@router.get("/callback")
def instagram_callback(code: str = None, error: str = None):
    if error:
        return JSONResponse({"status": "error", "message": error})

    data = {
        "client_id": INSTAGRAM_CLIENT_ID,
        "client_secret": INSTAGRAM_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    token_res = requests.post("https://api.instagram.com/oauth/access_token", data=data).json()
    access_token = token_res.get("access_token")

    user_info = requests.get(f"https://graph.instagram.com/me?fields=id,username&access_token={access_token}").json()
    save_token("instagram", user_info.get("id"), user_info.get("username"), None, access_token)
    return success_redirect()
