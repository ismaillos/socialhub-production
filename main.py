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
app = FastAPI(title="SocialHub (Real OAuth + Upgrades)", version="1.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
templates = Jinja2Templates(directory="templates")
def require_api_key(x_api_key: str = Header(None)):
    if not API_KEY or x_api_key != API_KEY: raise HTTPException(status_code=401, detail="Unauthorized")
@app.get("/", response_class=HTMLResponse)
def home(request: Request): return templates.TemplateResponse("index.html", {"request": request})
@app.get("/accounts", response_class=HTMLResponse)
def accounts(request: Request):
    with SessionLocal() as session: tokens = session.query(Token).all()
    return templates.TemplateResponse("accounts.html", {"request": request, "tokens": tokens})
@app.post("/disconnect/{platform}")
def disconnect(platform: str):
    with SessionLocal() as session:
        tok = session.query(Token).filter(Token.platform == platform).first()
        if not tok: raise HTTPException(status_code=404, detail=f"No account for {platform}")
        session.delete(tok); session.commit()
    return RedirectResponse(url="/accounts", status_code=302)
@app.get("/auth/status")
def auth_status():
    with SessionLocal() as session: tokens = session.query(Token).all(); connected = {t.platform: True for t in tokens}
    return JSONResponse(connected)
@app.get("/token/{platform}")
def get_token(platform: str, x_api_key: str = Header(None)):
    require_api_key(x_api_key)
    with SessionLocal() as session:
        t = session.query(Token).filter(Token.platform == platform).first()
        if not t: raise HTTPException(status_code=404, detail="Not connected")
        return {"platform": t.platform,"account_id": t.account_id,"username": t.username,"business_id": t.business_id,"page_id": t.page_id,"access_token": t.access_token,"page_access_token": t.page_access_token,"refresh_token": t.refresh_token}
@app.post("/publish")
async def publish(request: Request):
    data = await request.json(); platform = data.get("platform"); message = data.get("message"); media_url = data.get("media_url")
    with SessionLocal() as session:
        token = session.query(Token).filter(Token.platform == platform).first()
        if not token: raise HTTPException(status_code=404, detail="No connected account found")
        post = Post(platform=platform, account_id=token.account_id, message=message, media_url=media_url); session.add(post); session.commit()
    return JSONResponse({"status": "ok", "platform": platform, "message": message})
@app.get("/health")
def health(): return {"status": "ok", "uptime": datetime.datetime.utcnow().isoformat()}
app.include_router(facebook.router); app.include_router(instagram.router); app.include_router(tiktok.router); app.include_router(youtube.router)
REFRESH_DAYS_META = int(os.getenv("META_REFRESH_INTERVAL_DAYS", "50"))
FACEBOOK_CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID"); FACEBOOK_CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID"); GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
TIKTOK_CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY"); TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")
def refresh_meta_tokens_loop():
    while True:
        try:
            with SessionLocal() as session:
                metas = session.query(Token).filter(Token.platform.in_(["facebook","instagram"])).all()
                for mt in metas:
                    if not mt.access_token: continue
                    params = {"grant_type": "fb_exchange_token","client_id": FACEBOOK_CLIENT_ID,"client_secret": FACEBOOK_CLIENT_SECRET,"fb_exchange_token": mt.access_token}
                    res = requests.get("https://graph.facebook.com/v19.0/oauth/access_token", params=params).json()
                    new_token = res.get("access_token")
                    if new_token:
                        mt.access_token = new_token
                        if mt.page_id:
                            page_info = requests.get(f"https://graph.facebook.com/{mt.page_id}", params={"fields": "access_token", "access_token": new_token}).json()
                            if "access_token" in page_info: mt.page_access_token = page_info["access_token"]
                        session.add(mt); session.commit()
        except Exception as e: print("[META_REFRESH_ERR]", e)
        time.sleep(REFRESH_DAYS_META * 24 * 3600)
def refresh_google_tokens_loop():
    while True:
        try:
            with SessionLocal() as session:
                yt = session.query(Token).filter(Token.platform=="youtube", Token.refresh_token!=None).all()
                for y in yt:
                    data = {"client_id": GOOGLE_CLIENT_ID,"client_secret": GOOGLE_CLIENT_SECRET,"refresh_token": y.refresh_token,"grant_type": "refresh_token"}
                    res = requests.post("https://oauth2.googleapis.com/token", data=data).json()
                    if res.get("access_token"): y.access_token = res["access_token"]; session.add(y); session.commit()
        except Exception as e: print("[GOOGLE_REFRESH_ERR]", e)
        time.sleep(24 * 3600)
def refresh_tiktok_tokens_loop():
    while True:
        try:
            with SessionLocal() as session:
                tks = session.query(Token).filter(Token.platform=="tiktok", Token.refresh_token!=None).all()
                for tk in tks:
                    data = {"client_key": TIKTOK_CLIENT_KEY,"client_secret": TIKTOK_CLIENT_SECRET,"grant_type": "refresh_token","refresh_token": tk.refresh_token}
                    res = requests.post("https://open-api.tiktok.com/oauth/refresh_token/", data=data).json()
                    if res.get("data"):
                        new_at = res["data"].get("access_token"); new_rt = res["data"].get("refresh_token") or tk.refresh_token
                        if new_at: tk.access_token = new_at; tk.refresh_token = new_rt; session.add(tk); session.commit()
        except Exception as e: print("[TIKTOK_REFRESH_ERR]", e)
        time.sleep(24 * 3600)
@app.on_event("startup")
def on_startup():
    if FACEBOOK_CLIENT_ID and FACEBOOK_CLIENT_SECRET: threading.Thread(target=refresh_meta_tokens_loop, daemon=True).start()
    if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET: threading.Thread(target=refresh_google_tokens_loop, daemon=True).start()
    if TIKTOK_CLIENT_KEY and TIKTOK_CLIENT_SECRET: threading.Thread(target=refresh_tiktok_tokens_loop, daemon=True).start()
