# auth/bluesky.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
import requests
import os

router = APIRouter(prefix="/auth/bluesky", tags=["Bluesky"])

# -----------------------------------
# 🔧 Bluesky Configuration
# -----------------------------------
# Bluesky App Password authentication (no OAuth)
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE", "")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD", "")
BLUESKY_API_URL = "https://bsky.social/xrpc/com.atproto.server.createSession"


# -----------------------------------
# 1️⃣ Bluesky Login (Simulated or Real)
# -----------------------------------
@router.get("/login")
async def login():
    """
    Bluesky doesn't use OAuth yet (as of 2025).
    You authenticate using your handle and app password.

    - For production: user enters handle/password in frontend (form).
    - For local testing: use env vars BLUESKY_HANDLE and BLUESKY_PASSWORD.
    """
    if BLUESKY_HANDLE and BLUESKY_PASSWORD:
        # Attempt real Bluesky login
        payload = {
            "identifier": BLUESKY_HANDLE,
            "password": BLUESKY_PASSWORD
        }
        try:
            res = requests.post(BLUESKY_API_URL, json=payload, timeout=10)
            if res.status_code == 200:
                data = res.json()
                return JSONResponse({
                    "status": "ok",
                    "platform": "bluesky",
                    "handle": BLUESKY_HANDLE,
                    "accessJwt": data.get("accessJwt"),
                    "refreshJwt": data.get("refreshJwt"),
                    "did": data.get("did"),
                    "message": "Bluesky login successful ✅"
                })
            else:
                return JSONResponse({
                    "status": "error",
                    "platform": "bluesky",
                    "response": res.text,
                    "message": "Bluesky authentication failed ❌"
                })
        except Exception as e:
            return JSONResponse({"status": "error", "message": str(e)})

    # Simulated (no credentials)
    return JSONResponse({
        "status": "ok",
        "platform": "bluesky",
        "message": "Bluesky login simulated ✅ (no handle/password set)"
    })


# -----------------------------------
# 2️⃣ Optional: POST login (for manual handle/password)
# -----------------------------------
@router.post("/login")
async def login_post(handle: str = Form(...), password: str = Form(...)):
    """
    Accepts Bluesky credentials via POST form.
    """
    payload = {"identifier": handle, "password": password}
    try:
        res = requests.post(BLUESKY_API_URL, json=payload, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return JSONResponse({
                "status": "ok",
                "platform": "bluesky",
                "handle": handle,
                "accessJwt": data.get("accessJwt"),
                "refreshJwt": data.get("refreshJwt"),
                "did": data.get("did"),
                "message": "Bluesky session created ✅"
            })
        else:
            return JSONResponse({
                "status": "error",
                "response": res.text,
                "message": "Failed to authenticate with Bluesky ❌"
            })
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})
