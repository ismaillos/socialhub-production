# auth/instagram.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/auth/instagram", tags=["Instagram"])

@router.get("/login")
async def login():
    # In production, redirect to Instagram OAuth URL
    return JSONResponse({"status": "ok", "platform": "instagram", "message": "Instagram login simulated ✅"})

@router.get("/callback")
async def callback(code: str = None):
    if not code:
        return JSONResponse({"status": "error", "message": "Missing code"})
    # Here you'd normally exchange the code for an access token
    return JSONResponse({"status": "ok", "token": "fake_instagram_token"})
