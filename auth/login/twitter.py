# auth/twitter.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
import os
import requests
import urllib.parse

router = APIRouter(prefix="/auth/twitter", tags=["Twitter / X"])

# -----------------------------------
# 🔧 Twitter API Configuration
# -----------------------------------
TWITTER_CLIENT_ID = os.getenv("TWITTER_CLIENT_ID", "your_twitter_client_id")
TWITTER_CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET", "your_twitter_client_secret")
TWITTER_REDIRECT_URI = os.getenv(
    "TWITTER_REDIRECT_URI",
    "https://socialhub-production-production.up.railway.app/auth/twitter/callback",
)
TWITTER_SCOPE = "tweet.read tweet.write users.read offline.access"

TWITTER_AUTH_URL = "https://twitter.com/i/oauth2/authorize"
TWITTER_TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
TWITTER_USER_URL = "https://api.twitter.com/2/users/me"

# -----------------------------------
# 1️⃣ Twitter Login (Redirect to OAuth)
# -----------------------------------
@router.get("/login")
async def login():
    """
    Redirect user to Twitter OAuth2 authorization page.
    If client_id is not set, simulate login.
    """
    if TWITTER_CLIENT_ID == "your_twitter_client_id":
        return JSONResponse({
            "status": "ok",
            "platform": "twitter",
            "message": "Twitter login simulated ✅ (no API keys set)"
        })

    state = "secure_random_state_12345"
    params = {
        "response_type": "code",
        "client_id": TWITTER_CLIENT_ID,
        "redirect_uri": TWITTER_REDIRECT_URI,
        "scope": TWITTER_SCOPE,
        "state": state,
        "code_challenge": "challenge123",  # Optional PKCE
        "code_challenge_method": "plain",
    }

    url = f"{TWITTER_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)


# -----------------------------------
# 2️⃣ Twitter Callback (Exchange Code)
# -----------------------------------
@router.get("/callback")
async def callback(code: str = None, error: str = None):
    """
    Exchange authorization code for access token.
    """
    if error:
        return JSONResponse({"status": "error", "message": f"Twitter OAuth failed: {error}"})

    if not code:
        return JSONResponse({"status": "error", "message": "Missing authorization code from Twitter"})

    try:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": TWITTER_REDIRECT_URI,
            "client_id": TWITTER_CLIENT_ID,
            "code_verifier": "challenge123",
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(TWITTER_TOKEN_URL, data=data, headers=headers, auth=(TWITTER_CLIENT_ID, TWITTER_CLIENT_SECRET))
        token_data = response.json()

        if "access_token" not in token_data:
            return JSONResponse({"status": "error", "response": token_data, "message": "Failed to get Twitter access token"})

        access_token = token_data["access_token"]

        # Fetch user info
        user_response = requests.get(
            TWITTER_USER_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_response.json()

        return JSONResponse({
            "status": "ok",
            "platform": "twitter",
            "access_token": access_token,
            "refresh_token": token_data.get("refresh_token"),
            "user": user_data,
            "message": "Twitter login successful ✅"
        })

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})


# -----------------------------------
# 3️⃣ Simulated Login (Optional)
# -----------------------------------
@router.get("/simulate")
async def simulate():
    """
    Simulated Twitter login (no API key required).
    """
    return JSONResponse({
        "status": "ok",
        "platform": "twitter",
        "message": "Twitter login simulated ✅"
    })
