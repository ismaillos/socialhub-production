
from fastapi import APIRouter, Request, Form, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from utils.media_handler import (
    post_to_facebook, post_to_instagram, post_to_tiktok, post_to_youtube
)
from utils.encryption import decrypt_value
from sqlmodel import Session, select
from models.user_settings import UserSettings
from config import settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
def show_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.post("/dashboard/post")
async def dashboard_post(
    request: Request,
    user_id: str = Form(...),
    message: str = Form(...),
    media: UploadFile = None
):
    with Session(settings.engine) as session:
        user = session.exec(select(UserSettings).where(UserSettings.user_id == user_id)).first()
        if not user:
            return {"error": "User not found"}
        tokens = {
            "facebook": decrypt_value(user.facebook_token) if user.facebook_token else None,
            "instagram": decrypt_value(user.instagram_token) if user.instagram_token else None,
            "tiktok": decrypt_value(user.tiktok_token) if user.tiktok_token else None,
            "youtube": decrypt_value(user.youtube_token) if user.youtube_token else None
        }

    results = {}
    if tokens["facebook"]:
        results["facebook"] = await post_to_facebook(tokens["facebook"], message, media)
    if tokens["instagram"]:
        results["instagram"] = await post_to_instagram(tokens["instagram"], message, media)
    if tokens["tiktok"]:
        results["tiktok"] = await post_to_tiktok(tokens["tiktok"], message, media)
    if tokens["youtube"]:
        results["youtube"] = await post_to_youtube(tokens["youtube"], message, media)

    return results
