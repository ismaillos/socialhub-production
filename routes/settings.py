import os
from fastapi import APIRouter, Header, HTTPException, Form, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db.database import SessionLocal
from db.models import AppSecret
from util.secret_box import encrypt_value
from core.config import get_secret
router=APIRouter(prefix='/settings', tags=['Settings'])
templates=Jinja2Templates(directory='templates')
def _get_api_key()->str|None:
    return os.getenv('API_KEY') or get_secret('API_KEY')
def _require(request:Request, x_api_key:str|None):
    provided=x_api_key or request.cookies.get('x_api_key')
    stored=_get_api_key()
    if not stored: raise HTTPException(428,'API key not set (bootstrap required)')
    if provided!=stored: raise HTTPException(401,'Unauthorized')
@router.get('/login', response_class=HTMLResponse)
def login_page(request:Request): return templates.TemplateResponse('login.html', {'request':request})
@router.post('/login')
def login(request:Request, response:Response, api_key:str=Form(...)):
    stored=_get_api_key()
    if not stored: return RedirectResponse('/settings/bootstrap',302)
    if api_key!=stored: return templates.TemplateResponse('login.html', {'request':request,'error':'Invalid API key'}, status_code=401)
    r=RedirectResponse('/settings',302); r.set_cookie('x_api_key', api_key, httponly=True, secure=True, samesite='Lax', max_age=60*60*24*30); return r
@router.get('/bootstrap', response_class=HTMLResponse)
def bootstrap(request:Request):
    if _get_api_key(): return RedirectResponse('/settings',302)
    return templates.TemplateResponse('bootstrap.html', {'request':request})
@router.post('/bootstrap')
def bootstrap_set(api_key:str=Form(...)):
    if _get_api_key(): return RedirectResponse('/settings',302)
    enc=encrypt_value(api_key)
    with SessionLocal() as s: s.add(AppSecret(key='API_KEY', value_enc=enc)); s.commit()
    return RedirectResponse('/settings/login',302)
@router.get('', response_class=HTMLResponse)
def page(request:Request, x_api_key:str|None=Header(None)):
    try: _require(request, x_api_key)
    except HTTPException as e:
        if e.status_code==428: return RedirectResponse('/settings/bootstrap',302)
        raise
    with SessionLocal() as s: secrets=s.query(AppSecret).all()
    return templates.TemplateResponse('settings.html', {'request':request,'secrets':secrets})
@router.post('/secret')
def upsert(request:Request, key:str=Form(...), value:str=Form(...), x_api_key:str|None=Header(None)):
    _require(request, x_api_key)
    enc=encrypt_value(value)
    with SessionLocal() as s:
        row=s.query(AppSecret).filter(AppSecret.key==key).first()
        if row: row.value_enc=enc
        else: s.add(AppSecret(key=key, value_enc=enc))
        s.commit()
    return RedirectResponse('/settings',302)
@router.delete('/secret/{key}')
def delete(request:Request, key:str, x_api_key:str|None=Header(None)):
    _require(request, x_api_key)
    with SessionLocal() as s:
        row=s.query(AppSecret).filter(AppSecret.key==key).first()
        if row: s.delete(row); s.commit()
    return JSONResponse({'status':'ok'})
@router.get('/quick', response_class=HTMLResponse)
def quick(request:Request, x_api_key:str|None=Header(None)):
    return templates.TemplateResponse('settings_quick.html', {'request':request})
