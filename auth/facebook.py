# auth/facebook.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/auth/facebook", tags=["Facebook"])

@router.get("/login")
async def login():
    # Here you'd normally redirect to Facebook OAuth URL
    return JSONResponse({"status": "ok", "platform": "facebook", "message": "Facebook login simulated ✅"})

@router.get("/callback")
async def callback(code: str = None):
    if not code:
        return JSONResponse({"status": "error", "message": "Missing code"})
    # Normally you would exchange `code` for an access token
    return JSONResponse({"status": "ok", "token": "fake_facebook_token"})
