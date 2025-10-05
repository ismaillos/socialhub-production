import os
import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from db.database import Base, engine, SessionLocal
from db.models import Token, Post

# ✅ Import social auth routers dynamically
try:
    from auth import facebook, instagram, linkedin, twitter, tiktok, youtube, pinterest, bluesky
except ImportError:
    facebook = instagram = linkedin = twitter = tiktok = youtube = pinterest = bluesky = None
    print("[⚠️] One or more auth modules missing. Simulation mode only.")

# ✅ Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SocialHub Production", version="2.0.0")

# ✅ Enable CORS (for n8n and web dashboard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to your domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# ----------------------------
# 🔹 ROUTES
# ----------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Dashboard landing page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/accounts", response_class=HTMLResponse)
def accounts(request: Request):
    """Show connected social accounts"""
    with SessionLocal() as session:
        tokens = session.query(Token).all()
    return templates.TemplateResponse("accounts.html", {"request": request, "tokens": tokens})


@app.get("/logs", response_class=HTMLResponse)
def logs(request: Request):
    """Show recent post logs"""
    with SessionLocal() as session:
        posts = session.query(Post).order_by(Post.timestamp.desc()).all()
    return templates.TemplateResponse("logs.html", {"request": request, "posts": posts})


@app.post("/publish")
async def publish(request: Request):
    """Used by n8n to post content to connected accounts"""
    data = await request.json()
    platform = data.get("platform")
    message = data.get("message")
    media_url = data.get("media_url")

    with SessionLocal() as session:
        token = session.query(Token).filter(Token.platform == platform).first()
        if not token:
            raise HTTPException(status_code=404, detail="No connected account found for this platform")

        print(f"[PUBLISH] {platform}: {message}")
        post = Post(platform=platform, account_id=token.account_id, message=message, media_url=media_url)
        session.add(post)
        session.commit()

    return JSONResponse({"status": "success", "platform": platform, "message": message})


# ----------------------------
# 🔹 DISCONNECT ROUTE
# ----------------------------
@app.post("/disconnect/{platform}")
def disconnect(platform: str):
    """Remove OAuth credentials for a given platform"""
    with SessionLocal() as session:
        token = session.query(Token).filter(Token.platform == platform).first()
        if not token:
            raise HTTPException(status_code=404, detail=f"No connected account for {platform}")
        session.delete(token)
        session.commit()
    print(f"[DISCONNECT] Removed {platform} token.")
    return RedirectResponse(url="/accounts", status_code=302)


# ----------------------------
# 🔹 AUTH STATUS
# ----------------------------
@app.get("/auth/status")
def auth_status():
    """Return list of connected accounts (used by frontend to show status)"""
    with SessionLocal() as session:
        tokens = session.query(Token).all()
        connected = {t.platform: True for t in tokens}
    return JSONResponse(connected)


# ----------------------------
# 🔹 REGISTER AUTH ROUTERS
# ----------------------------
if facebook: app.include_router(facebook.router)
if instagram: app.include_router(instagram.router)
if linkedin: app.include_router(linkedin.router)
if twitter: app.include_router(twitter.router)
if tiktok: app.include_router(tiktok.router)
if youtube: app.include_router(youtube.router)
if pinterest: app.include_router(pinterest.router)
if bluesky: app.include_router(bluesky.router)


# ----------------------------
# 🔹 HEALTH CHECK
# ----------------------------
@app.get("/health")
def health():
    """Simple uptime check"""
    return {"status": "ok", "uptime": datetime.datetime.utcnow().isoformat()}


# ----------------------------
# 🔹 OPTIONAL: CLEANUP ROUTE
# ----------------------------
@app.post("/reset")
def reset_all():
    """⚠️ Dev-only: delete all tokens/posts (use carefully)"""
    with SessionLocal() as session:
        deleted_tokens = session.query(Token).delete()
        deleted_posts = session.query(Post).delete()
        session.commit()
    return {"status": "reset", "deleted_tokens": deleted_tokens, "deleted_posts": deleted_posts}
