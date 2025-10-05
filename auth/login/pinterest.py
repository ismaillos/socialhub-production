# auth/pinterest.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
import os
import urllib.parse
import requests

router = APIRouter(prefix="/auth/pinterest", tags=["Pinterest"])

# -----------------------------------
# 🔧 Pinterest OAuth2 Configuration
# -----------------------------------
PINTEREST_CLIENT_ID = os.getenv("PINTEREST_CLIENT_ID", "your_pinterest_client_id")
PINTEREST_CLIENT_SECRET = os.getenv("PINTEREST_CLIENT_SECRET", "your_pinterest_client_secret")
PINTEREST_REDIRECT_URI = os.getenv(
    "PINTEREST_REDIRECT_URI",
    "https://socialhub-production-production.up.railway.app/auth/pinterest/callback",
)

PINTEREST_AUTH_URL = "https://www.pinterest.com/oauth/"
PINTEREST_TOKEN_URL = "https://api.pinterest.com/v5/oauth/token"
PINTEREST_SCOPE = "boards:read,pins:read,pins:write,user_accounts:read"


# -----------------------------------
# 1️⃣ Pinterest Login (Redirect to OAuth)
# -----------------------------------
@router.get("/login")
async def login():
    """
    Redirect user to Pinterest's OAuth2 authorization screen.
    """
    params = {
        "response_type": "code",
        "client_id": PINTEREST_CLIENT_ID,
        "redirect_uri": PINTEREST_REDIRECT_URI,
        "scope": PINTEREST_SCOPE,
        "state": "secure_random_state_12345",
    }
    url = f"{PINTEREST_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)


# -----------------------------------
# 2️⃣ Pinterest Callback (Exchange Code)
# -----------------------------------
@router.get("/callback")
async def callback(code: str = None, error: str = None):
    """
    Handle Pinterest OAuth callback and exchange code for an access token.
    """
    if error:
        return JSONResponse({"status": "error", "message": f"Pinterest OAuth failed: {error}"})
    if not code:
        return JSONResponse({"status": "error", "message": "Missing authorization code from Pinterest"})

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": PINTEREST_REDIRECT_URI,
        "client_id": PINTEREST_CLIENT_ID,
        "client_secret": PINTEREST_CLIENT_SECRET,
    }

    try:
        response = requests.post(PINTEREST_TOKEN_URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        token_json = response.json()

        if "access_token" not in token_json:
            return JSONResponse({"status": "error", "response": token_json, "message": "Failed to get Pinterest access token"})

        access_token = token_json["access_token"]

        # Optional: Fetch user info
        user_response = requests.get(
            "https://api.pinterest.com/v5/user_account",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_json = user_response.json()

        return JSONResponse({
            "status": "ok",
            "platform": "pinterest",
            "access_token": access_token,
            "user": user_json,
            "message": "Pinterest login successful ✅"
        })
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})


# -----------------------------------
# 3️⃣ Simulated Login (Optional for Local Testing)
# -----------------------------------
@router.get("/simulate")
async def simulate():
    """
    For local testing without real Pinterest OAuth credentials.
    """
    return JSONResponse({
        "status": "ok",
        "platform": "pinterest",
        "message": "Pinterest login simulated ✅ (no real OAuth)"
    })
