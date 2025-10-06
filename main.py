import os
import threading
import time
import datetime
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from db.database import Base, engine, SessionLocal
from db.models import Token, Post
from auth import facebook, instagram, tiktok, youtube

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SocialHub (Real OAuth)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/accounts", response_class=HTMLResponse)
def accounts(request: Request):
    with SessionLocal() as session:
        tokens = session.query(Token).all()
    return templates.TemplateResponse("accounts.html", {"request": request, "tokens": tokens})

@app.post("/disconnect/{platform}")
def disconnect(platform: str):
    with SessionLocal() as session:
        tok = session.query(Token).filter(Token.platform == platform).first()
        if not tok:
            raise HTTPException(status_code=404, detail=f"No account for {platform}")
        session.delete(tok)
        session.commit()
    return RedirectResponse(url="/accounts", status_code=302)

@app.get("/auth/status")
def auth_status():
    with SessionLocal() as session:
        tokens = session.query(Token).all()
        connected = {t.platform: True for t in tokens}
    return JSONResponse(connected)

@app.post("/publish")
async def publish(request: Request):
    data = await request.json()
    platform = data.get("platform")
    message = data.get("message")
    media_url = data.get("media_url")

    with SessionLocal() as session:
        token = session.query(Token).filter(Token.platform == platform).first()
        if not token:
            raise HTTPException(status_code=404, detail="No connected account found")

        # NOTE: This demo only logs the post; integrate platform-specific publishing in n8n using stored tokens/ids.
        post = Post(platform=platform, account_id=token.account_id, message=message, media_url=media_url)
        session.add(post)
        session.commit()

    return JSONResponse({"status": "ok", "platform": platform, "message": message})

@app.get("/health")
def health():
    return {"status": "ok", "uptime": datetime.datetime.utcnow().isoformat()}

# Include OAuth routers
app.include_router(facebook.router)
app.include_router(instagram.router)
app.include_router(tiktok.router)
app.include_router(youtube.router)

# ---------------- Long-lived Meta Token Refresher ----------------
REFRESH_DAYS = int(os.getenv("META_REFRESH_INTERVAL_DAYS", "50"))
FACEBOOK_CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID")
FACEBOOK_CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET")

def refresh_meta_tokens_loop():
    while True:
        try:
            with SessionLocal() as session:
                meta_tokens = session.query(Token).filter(Token.platform.in_(["facebook", "instagram"])).all()
                for mt in meta_tokens:
                    if not mt.access_token:
                        continue
                    # Exchange for long-lived token
                    params = {
                        "grant_type": "fb_exchange_token",
                        "client_id": FACEBOOK_CLIENT_ID,
                        "client_secret": FACEBOOK_CLIENT_SECRET,
                        "fb_exchange_token": mt.access_token,
                    }
                    res = requests.get("https://graph.facebook.com/v19.0/oauth/access_token", params=params).json()
                    new_token = res.get("access_token")
                    if new_token:
                        mt.access_token = new_token
                        # If we have a page_id, refresh page token as well
                        if mt.page_id:
                            page_info = requests.get(
                                f"https://graph.facebook.com/{mt.page_id}",
                                params={"fields": "access_token", "access_token": new_token},
                            ).json()
                            if "access_token" in page_info:
                                mt.page_access_token = page_info["access_token"]
                        session.add(mt)
                        session.commit()
        except Exception as e:
            print("[META_REFRESH_ERR]", e)
        # Sleep for configured days
        time.sleep(REFRESH_DAYS * 24 * 3600)

@app.on_event("startup")
def on_startup():
    # Kick off refresher (non-blocking)
    if FACEBOOK_CLIENT_ID and FACEBOOK_CLIENT_SECRET:
        thr = threading.Thread(target=refresh_meta_tokens_loop, daemon=True)
        thr.start()
