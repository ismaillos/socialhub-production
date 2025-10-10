
from fastapi import APIRouter, Request
from auth import facebook, instagram, youtube, tiktok

router = APIRouter()

@router.get("/facebook")
async def facebook_oauth_start(request: Request):
    return await facebook.facebook_login(request)

@router.get("/facebook/callback")
async def facebook_oauth_finish(request: Request):
    return await facebook.facebook_callback(request)

@router.get("/instagram")
async def instagram_oauth_start(request: Request):
    return await instagram.instagram_login(request)

@router.get("/instagram/callback")
async def instagram_oauth_finish(request: Request):
    return await instagram.instagram_callback(request)

@router.get("/youtube")
async def youtube_oauth_start(request: Request):
    return await youtube.youtube_login(request)

@router.get("/youtube/callback")
async def youtube_oauth_finish(request: Request):
    return await youtube.youtube_callback(request)

@router.get("/tiktok")
async def tiktok_oauth_start(request: Request):
    return await tiktok.tiktok_login(request)

@router.get("/tiktok/callback")
async def tiktok_oauth_finish(request: Request):
    return await tiktok.tiktok_callback(request)
