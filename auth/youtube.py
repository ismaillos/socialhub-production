# auth/youtube.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
import os
import urllib.parse
import requests

router = APIRouter(prefix="/auth/youtube", tags=["YouTube / Google"])

# -----------------------------------
# 🔧 YouTube OAuth2 Configuration
# -----------------------------------
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "your_youtube_client_id")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "your_youtube_client_secret")
YOUTUBE_REDIRECT_URI = os.getenv(
    "YOUTUBE_REDIRECT_URI",
    "https://socialhub-production-production.up.railway.app/auth/youtube/callback",
)

YOUTUBE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
YOUTUBE_TOKEN_URL = "https://oauth2.googleapis.com/token"
YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/userinfo.email"


# -----------------------------------
# 1️⃣ YouTube Login (Redirect to Google OAuth2)
# -----------------------------------
@router.get("/login")
async def login():
    """
    Redirect the user to Google's OAuth2 authorization screen for YouTube.
    """
    if YOUTUBE_CLIENT_ID == "your_youtube_client_id":
        return JSONResponse({
            "status": "ok",
            "platform": "youtube",
            "message": "YouTube login simulated ✅ (no credentials set)"
        })

    params = {
        "client_id": YOUTUBE_CLIENT_ID,
        "redirect_uri": YOUTUBE_REDIRECT_URI,
        "response_type": "code",
        "scope": YOUTUBE_SCOPE,
        "access_type": "offline",
        "prompt": "consent",
        "state": "secure_state_youtube123",
    }

    auth_url = f"{YOUTUBE_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(auth_url)


# -----------------------------------
# 2️⃣ YouTube Callback (Exchange Code for Token)
# -----------------------------------
@router.get("/callback")
async def callback(code: str = None, error: str = None):
    """
    Handle YouTube OAuth2 callback and exchange the code for access/refresh tokens.
    """
    if error:
        return JSONResponse({"status": "error", "message": f"YouTube OAuth failed: {error}"})

    if not code:
        return JSONResponse({"status": "error", "message": "Missing authorization code from YouTube"})

    data = {
        "code": code,
        "client_id": YOUTUBE_CLIENT_ID,
        "client_secret": YOUTUBE_CLIENT_SECRET,
        "redirect_uri": YOUTUBE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        token_res = requests.post(YOUTUBE_TOKEN_URL, data=data)
        token_json = token_res.json()

        if "access_token" not in token_json:
            return JSONResponse({
                "status": "error",
                "response": token_json,
                "message": "Failed to get YouTube access token"
            })

        access_token = token_json["access_token"]
        refresh_token = token_json.get("refresh_token")

        # Fetch YouTube channel info
        channel_res = requests.get(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        channel_json = channel_res.json()

        return JSONResponse({
            "status": "ok",
            "platform": "youtube",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "channel": channel_json,
            "message": "YouTube login successful ✅"
        })

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})


# -----------------------------------
# 3️⃣ Refresh Token Endpoint
# -----------------------------------
@router.get("/refresh")
async def refresh(refresh_token: str):
    """
    Refresh a YouTube access token using the saved refresh token.
    """
    data = {
        "client_id": YOUTUBE_CLIENT_ID,
        "client_secret": YOUTUBE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    try:
        res = requests.post(YOUTUBE_TOKEN_URL, data=data)
        token_json = res.json()
        return JSONResponse(token_json)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})
