from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse

router = APIRouter(prefix="/auth/facebook", tags=["Facebook"])

@router.get("/login")
def fb_login():
    return RedirectResponse(url="https://www.facebook.com/")

@router.get("/callback")
def fb_callback():
    return JSONResponse({"status": "ok", "platform": "facebook", "message": "Facebook simulated ✅"})
