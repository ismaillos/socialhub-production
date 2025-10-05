import os
import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from db.database import Base, engine, SessionLocal
from db.models import Token, Post

# ✅ Import routers dynamically
from auth import facebook, instagram, linkedin, twitter, tiktok, youtube, pinterest, bluesky

# ✅ Create DB tables automatically if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SocialHub Production", version="2.0.0")

# ✅ Enable CORS for n8n and other frontends
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
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/accounts", response_class=HTMLResponse)
def accounts(request: Request):
    with SessionLocal() as session:
        tokens = session.query(Token).all()
    return templates.TemplateResponse("accounts.html", {"request": request, "tokens": tokens})

@app.get("/logs", response_class=HTMLResponse)
def logs(request: Request):
    with SessionLocal() as session:
        posts = session.query(Post).order_by(Post.timestamp.desc()).all()
    return templates.TemplateResponse("logs.html", {"request": request, "posts": posts})

@app.post("/publish")
async def publish(request: Request):
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
# 🔹 REGISTER AUTH ROUTERS
# ----------------------------
app.include_router(facebook.router)
app.include_router(instagram.router)
app.include_router(linkedin.router)
app.include_router(twitter.router)
app.include_router(tiktok.router)
app.include_router(youtube.router)
app.include_router(pinterest.router)
app.include_router(bluesky.router)

# ----------------------------
# 🔹 HEALTH CHECK ENDPOINT
# ----------------------------
@app.get("/health")
def health():
    return {"status": "ok", "uptime": datetime.datetime.utcnow().isoformat()}
