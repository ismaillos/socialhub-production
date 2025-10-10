
from fastapi import APIRouter, Form, UploadFile
from utils.encryption import decrypt_value
from sqlmodel import Session, select
from config import settings
from models.user_settings import UserSettings
from utils.media_handler import (
    post_to_facebook, post_to_instagram,
    post_to_tiktok, post_to_youtube
)

router = APIRouter()

def get_tokens(user_id: str):
    with Session(settings.engine) as session:
        user = session.exec(select(UserSettings).where(UserSettings.user_id == user_id)).first()
        return {
            "facebook": decrypt_value(user.facebook_token) if user.facebook_token else None,
            "instagram": decrypt_value(user.instagram_token) if user.instagram_token else None,
            "tiktok": decrypt_value(user.tiktok_token) if user.tiktok_token else None,
            "youtube": decrypt_value(user.youtube_token) if user.youtube_token else None
        }

@router.post("/post")
async def post_all(
    user_id: str = Form(...),
    message: str = Form(...),
    media: UploadFile = None
):
    tokens = get_tokens(user_id)
    responses = {}
    if tokens['facebook']:
        responses['facebook'] = await post_to_facebook(tokens['facebook'], message, media)
    if tokens['instagram']:
        responses['instagram'] = await post_to_instagram(tokens['instagram'], message, media)
    if tokens['tiktok']:
        responses['tiktok'] = await post_to_tiktok(tokens['tiktok'], message, media)
    if tokens['youtube']:
        responses['youtube'] = await post_to_youtube(tokens['youtube'], message, media)
    return responses
