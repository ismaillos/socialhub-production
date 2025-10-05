from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse

router = APIRouter(prefix="/auth/youtube", tags=["YouTube"])

@router.get("/login")
def yt_login():
    return RedirectResponse(url="https://accounts.google.com/o/oauth2/v2/auth")

@router.get("/callback")
def yt_callback():
    return JSONResponse({"status": "ok", "platform": "youtube", "message": "YouTube simulated ✅"})
