import os, threading, time, datetime, requests
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from db.database import Base, engine, SessionLocal
from db.models import Token, Post
from auth import facebook, instagram, tiktok, youtube
API_KEY = os.getenv("API_KEY")
Base.metadata.create_all(bind=engine)
app = FastAPI(title="SocialHub", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
templates = Jinja2Templates(directory='templates')
def require_api_key(x_api_key: str = Header(None)):
    if not API_KEY or x_api_key != API_KEY: raise HTTPException(status_code=401, detail='Unauthorized')
@app.get('/', response_class=HTMLResponse)
def home(request: Request): return templates.TemplateResponse('index.html', {'request': request})
@app.get('/accounts', response_class=HTMLResponse)
def accounts(request: Request):
    with SessionLocal() as session: tokens = session.query(Token).all()
    return templates.TemplateResponse('accounts.html', {'request': request, 'tokens': tokens})
@app.post('/disconnect/{platform}')
def disconnect(platform: str):
    with SessionLocal() as session:
        tok = session.query(Token).filter(Token.platform == platform).first()
        if not tok: raise HTTPException(status_code=404, detail=f'No account for {platform}')
        session.delete(tok); session.commit()
    return RedirectResponse(url='/accounts', status_code=302)
@app.get('/auth/status')
def auth_status():
    with SessionLocal() as session:
        tokens = session.query(Token).all(); connected = {}
        for t in tokens: connected.setdefault(t.platform,0); connected[t.platform]+=1
    return JSONResponse(connected)
@app.get('/token/{platform}')
def list_tokens(platform: str, x_api_key: str = Header(None)):
    require_api_key(x_api_key)
    with SessionLocal() as s:
        rows = s.query(Token).filter(Token.platform == platform).all()
        return [{'platform': r.platform,'account_id': r.account_id,'username': r.username,'business_id': r.business_id,'page_id': r.page_id,'access_token': r.access_token,'page_access_token': r.page_access_token,'refresh_token': r.refresh_token} for r in rows]
@app.get('/token/{platform}/{account_id}')
def get_token(platform: str, account_id: str, x_api_key: str = Header(None)):
    require_api_key(x_api_key)
    with SessionLocal() as s:
        r = s.query(Token).filter(Token.platform == platform, Token.account_id == account_id).first()
        if not r: raise HTTPException(status_code=404, detail='Not connected')
        return {'platform': r.platform,'account_id': r.account_id,'username': r.username,'business_id': r.business_id,'page_id': r.page_id,'access_token': r.access_token,'page_access_token': r.page_access_token,'refresh_token': r.refresh_token}
@app.post('/publish')
async def publish(request: Request):
    data = await request.json(); platform = data.get('platform'); message = data.get('message'); media_url = data.get('media_url')
    with SessionLocal() as session:
        token = session.query(Token).filter(Token.platform == platform).first()
        if not token: raise HTTPException(status_code=404, detail='No connected account found')
        post = Post(platform=platform, account_id=token.account_id, message=message, media_url=media_url); session.add(post); session.commit()
    return JSONResponse({'status':'ok','platform':platform,'message':message})
@app.get('/health')
def health(): return {'status':'ok','uptime': datetime.datetime.utcnow().isoformat()}
app.include_router(facebook.router); app.include_router(instagram.router); app.include_router(tiktok.router); app.include_router(youtube.router)
from routes import settings as settings_routes
app.include_router(settings_routes.router)
