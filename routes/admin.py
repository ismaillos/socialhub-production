import os
from fastapi import APIRouter, Header, HTTPException, Query
from fastapi.responses import JSONResponse
from services.refresh import refresh_all, refresh_facebook_and_instagram, refresh_tiktok, refresh_youtube
from core.config import get_secret

router = APIRouter(prefix='/admin', tags=['Admin'])

def _check_cron(secret: str | None):
    cron_secret = get_secret('CRON_SECRET', os.getenv('CRON_SECRET'))
    if not cron_secret or secret != cron_secret:
        raise HTTPException(status_code=401, detail='Invalid CRON secret')

@router.post('/refresh')
def do_refresh(x_cron_secret: str | None = Header(None), platform: str | None = Query(None)):
    _check_cron(x_cron_secret)
    if not platform:
        return JSONResponse(refresh_all())
    platform = platform.lower()
    if platform in ('facebook','instagram','meta'):
        return JSONResponse(refresh_facebook_and_instagram())
    if platform == 'tiktok':
        return JSONResponse(refresh_tiktok())
    if platform == 'youtube':
        return JSONResponse(refresh_youtube())
    raise HTTPException(status_code=400, detail='Unknown platform')
