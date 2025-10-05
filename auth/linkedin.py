from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
import requests, os
from auth.oauth_utils import save_token, success_redirect

router = APIRouter(prefix="/auth/linkedin", tags=["LinkedIn"])

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "https://socialhub-production-production.up.railway.app/auth/linkedin/callback")

@router.get("/login")
def linkedin_login():
    scope = "r_liteprofile r_emailaddress w_member_social"
    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code&client_id={LINKEDIN_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&scope={scope}"
    )
    return RedirectResponse(url=auth_url)

@router.get("/callback")
def linkedin_callback(code: str = None, error: str = None):
    if error:
        return JSONResponse({"status": "error", "message": error})
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }
    token_res = requests.post(token_url, data=data).json()
    access_token = token_res.get("access_token")

    # Fetch user info
    headers = {"Authorization": f"Bearer {access_token}"}
    profile = requests.get("https://api.linkedin.com/v2/me", headers=headers).json()
    name = profile.get("localizedFirstName", "User")
    account_id = profile.get("id")

    # Save to DB
    save_token("linkedin", account_id, name, None, access_token)
    return success_redirect()
