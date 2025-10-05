# auth/facebook.py
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse

router = APIRouter(prefix="/auth/facebook", tags=["Facebook"])

# Temporary fake login redirect (for testing)
@router.get("/login")
async def facebook_login():
    # In production you'd redirect to Facebook OAuth URL
    return JSONResponse({"status": "ok", "message": "Facebook login simulated ✅"})

# Placeholder callback
@router.get("/callback")
async def facebook_callback(code: str = None):
    if not code:
        return JSONResponse({"status": "error", "message": "Missing code"})
    # Here you'd normally exchange code for access token
    return JSONResponse({"status": "ok", "token": "fake_facebook_token"})
