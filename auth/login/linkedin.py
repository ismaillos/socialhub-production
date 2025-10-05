from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
import os
import urllib.parse
import requests
from db.database import SessionLocal
from db.models import Token

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
# 1️⃣ LinkedIn Login
# -----------------------------------
@router.get("/login")
async def login():
    """
    Redirect user to LinkedIn OAuth authorization screen.
    """
    if LINKEDIN_CLIENT_ID == "your_linkedin_client_id":
        return JSONResponse({
            "status": "ok",
            "platform": "linkedin",
            "message": "LinkedIn login simulated ✅ (no API keys set)"
        })

    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "scope": LINKEDIN_SCOPE,
        "state": "secure_state_12345",
    }
    url = f"{LINKEDIN_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)


# -----------------------------------
# 2️⃣ LinkedIn Callback + Token Storage
# -----------------------------------
@router.get("/callback")
async def callback(code: str = None, error: str = None):
    """
    Handle OAuth2 callback, exchange code for access token, fetch user profile,
    and store or update credentials in the database.
    """
    if error:
        return JSONResponse({"status": "error", "message": f"LinkedIn OAuth failed: {error}"})
    if not code:
        return JSONResponse({"status": "error", "message": "Missing authorization code"})

    # Exchange code for access token
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }

    try:
        token_response = requests.post(LINKEDIN_TOKEN_URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        token_json = token_response.json()

        if "access_token" not in token_json:
            return JSONResponse({"status": "error", "response": token_json, "message": "Failed to get LinkedIn access token"})

        access_token = token_json["access_token"]

        # Fetch LinkedIn user profile
        profile_response = requests.get(
            "https://api.linkedin.com/v2/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        profile_json = profile_response.json()

        account_id = profile_json.get("id", "unknown")

        # ✅ Save or update token in DB
        session = SessionLocal()
        existing = session.query(Token).filter(Token.platform == "linkedin").first()
        if existing:
            existing.access_token = access_token
            existing.account_id = account_id
            session.commit()
        else:
            new_token = Token(platform="linkedin", account_id=account_id, access_token=access_token)
            session.add(new_token)
            session.commit()
        session.close()

        return JSONResponse({
            "status": "ok",
            "platform": "linkedin",
            "account_id": account_id,
            "access_token": access_token,
            "profile": profile_json,
            "message": "LinkedIn login successful ✅ and token saved to DB"
        })

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})


# -----------------------------------
# 3️⃣ Simulated Login (Optional)
# -----------------------------------
@router.get("/simulate")
async def simulate():
    """
    Simulated LinkedIn login for local testing (no OAuth required).
    """
    return JSONResponse({
        "status": "ok",
        "platform": "linkedin",
        "account_id": "simulated_12345",
        "access_token": "fake_token_abc",
        "message": "LinkedIn login simulated ✅"
    })
