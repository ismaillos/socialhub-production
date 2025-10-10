import os, datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler
from db.database import Base, engine, SessionLocal
from db import models as db_models
Base.metadata.create_all(bind=engine)
from db.models import Token, Post
app=FastAPI(title='SocialHub',version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
templates=Jinja2Templates(directory='templates')
@app.get('/', response_class=HTMLResponse)
def home(request:Request): return templates.TemplateResponse('index.html', {'request':request})
@app.get('/accounts', response_class=HTMLResponse)
def accounts(request:Request):
    with SessionLocal() as s: tokens=s.query(Token).all()
    return templates.TemplateResponse('accounts.html', {'request':request,'tokens':tokens})
@app.get('/health') 
def health(): return {'status':'ok','uptime': datetime.datetime.utcnow().isoformat()}
from auth import facebook, instagram, tiktok, youtube
app.include_router(facebook.router); app.include_router(instagram.router); app.include_router(tiktok.router); app.include_router(youtube.router)
from routes import settings as settings_routes, admin as admin_routes, publish as publish_routes
app.include_router(settings_routes.router); app.include_router(admin_routes.router); app.include_router(publish_routes.router)
def _schedule_refresh():
    from services.refresh import refresh_all
    try: print('[Scheduler] refresh:', refresh_all(), flush=True)
    except Exception as e: print('[Scheduler] error:', e, flush=True)
if os.getenv('REFRESH_CRON_ENABLED','0')=='1':
    scheduler=BackgroundScheduler(timezone='UTC'); scheduler.add_job(_schedule_refresh,'interval',days=5,id='token_refresh',replace_existing=True); scheduler.start()
