import os
from fastapi import APIRouter, Header, HTTPException, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db.database import SessionLocal
from db.models import AppSecret
from util.secret_box import encrypt_value
router = APIRouter(prefix='/settings', tags=['Settings'])
templates = Jinja2Templates(directory='templates')
API_KEY = os.getenv('API_KEY')
def _require_api_key(x_api_key: str | None):
    if not API_KEY or x_api_key != API_KEY: raise HTTPException(status_code=401, detail='Unauthorized')
@router.get('', response_class=HTMLResponse)
def settings_page(request: Request, x_api_key: str | None = Header(None)):
    _require_api_key(x_api_key)
    with SessionLocal() as s: secrets = s.query(AppSecret).all()
    return templates.TemplateResponse('settings.html', {'request': request, 'secrets': secrets})
@router.post('/secret')
def upsert_secret(key: str = Form(...), value: str = Form(...), x_api_key: str | None = Header(None)):
    _require_api_key(x_api_key)
    enc = encrypt_value(value)
    with SessionLocal() as s:
        row = s.query(AppSecret).filter(AppSecret.key == key).first()
        if row: row.value_enc = enc
        else: s.add(AppSecret(key=key, value_enc=enc))
        s.commit()
    return RedirectResponse(url='/settings', status_code=302)
@router.delete('/secret/{key}')
def delete_secret(key: str, x_api_key: str | None = Header(None)):
    _require_api_key(x_api_key)
    with SessionLocal() as s:
        row = s.query(AppSecret).filter(AppSecret.key == key).first()
        if row: s.delete(row); s.commit()
    return JSONResponse({'status':'ok'})
