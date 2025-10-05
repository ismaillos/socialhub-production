from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse

router = APIRouter(prefix="/auth/tiktok", tags=["TikTok"])

@router.get("/login")
def tiktok_login():
    return RedirectResponse(url="https://www.tiktok.com/")

@router.get("/callback")
def tiktok_callback():
    return JSONResponse({"status": "ok", "platform": "tiktok", "message": "TikTok simulated ✅"})
