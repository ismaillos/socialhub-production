# auth/linkedin.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
import os
import urllib.parse
import requests

router = APIRouter(prefix="/auth/linkedin", tags=["LinkedIn"])

# -----------------------------------
# 🔧 LinkedIn OAuth2 Configuration
# -----------------------------------
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "your_linkedin_client_id")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "your_linkedin_client_secret")
LINKEDIN_REDIRECT_URI = os.getenv(
    "LINKEDIN_REDIRECT_URI",
    "https://socialhub-production-production.up.railway.app/auth/linkedin/callback",
)

LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_SCOPE = "r_liteprofile r_emailaddress w_member_social"


# -----------------------------------
# 1️⃣ LinkedIn Login Route
# -----------------------------------
@router.get("/login")
async def login():
    """
    Redirect the user to LinkedIn's OAuth2 authorization page.
    """
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "scope": LINKEDIN_SCOPE,
    }
    url = f"{LINKEDIN_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)


# -----------------------------------
# 2️⃣ LinkedIn Callback Route
# -----------------------------------
@router.get("/callback")
async def callback(code: str = None, error: str = None):
    """
    Handle LinkedIn OAuth2 callback and exchange authorization code for access token.
    """
    if error:
        return JSONResponse({"status": "error", "message": f"LinkedIn OAuth failed: {error}"})
    if not code:
        return JSONResponse({"status": "error", "message": "Missing authorization code from LinkedIn"})

    # Exchange code for access token
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }

    try:
        response = requests.post(LINKEDIN_TOKEN_URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        token_json = response.json()

        if "access_token" not in token_json:
            return JSONResponse({"status": "error", "response": token_json, "message": "Failed to get LinkedIn access token"})

        access_token = token_json["access_token"]

        # Optional: Get LinkedIn profile
        profile_response = requests.get(
            "https://api.linkedin.com/v2/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        profile_json = profile_response.json()

        return JSONResponse({
            "status": "ok",
            "platform": "linkedin",
            "access_token": access_token,
            "profile": profile_json,
            "message": "LinkedIn login successful ✅"
        })
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})
