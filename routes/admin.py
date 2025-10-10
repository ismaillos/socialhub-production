import os
from fastapi import APIRouter, Header, HTTPException, Query
from fastapi.responses import JSONResponse
from services.refresh import refresh_all, refresh_facebook_and_instagram, refresh_tiktok, refresh_youtube
from core.config import get_secret
router=APIRouter(prefix='/admin', tags=['Admin'])
def _check(secret:str|None):
    cron=get_secret('CRON_SECRET', os.getenv('CRON_SECRET'))
    if not cron or secret!=cron: raise HTTPException(status_code=401, detail='Invalid CRON secret')
@router.post('/refresh')
def refresh(x_cron_secret:str|None=Header(None), platform:str|None=Query(None)):
    _check(x_cron_secret)
    if not platform: return JSONResponse(refresh_all())
    p=platform.lower()
    if p in ('facebook','instagram','meta'): return JSONResponse(refresh_facebook_and_instagram())
    if p=='tiktok': return JSONResponse(refresh_tiktok())
    if p=='youtube': return JSONResponse(refresh_youtube())
    raise HTTPException(400,'Unknown platform')
