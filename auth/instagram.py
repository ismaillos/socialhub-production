from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse

router = APIRouter(prefix="/auth/instagram", tags=["Instagram"])

@router.get("/login")
def ig_login():
    return RedirectResponse(url="https://www.instagram.com/")

@router.get("/callback")
def ig_callback():
    return JSONResponse({"status": "ok", "platform": "instagram", "message": "Instagram simulated ✅"})
