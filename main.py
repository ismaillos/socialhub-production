from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from db.database import Base, engine, SessionLocal
from db.models import Token, Post

# 👇 Add this import line near the top
from auth import facebook, instagram, linkedin, twitter, tiktok, youtube, pinterest, bluesky

import datetime

app = FastAPI(title="SocialHub Production", version="1.0.0")
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

# ----------------------
# 🔹 EXISTING ROUTES
# ----------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/accounts", response_class=HTMLResponse)
def accounts(request: Request):
    session = SessionLocal()
    tokens = session.query(Token).all()
    session.close()
    return templates.TemplateResponse("accounts.html", {"request": request, "tokens": tokens})

@app.get("/logs", response_class=HTMLResponse)
def logs(request: Request):
    session = SessionLocal()
    posts = session.query(Post).order_by(Post.timestamp.desc()).all()
    session.close()
    return templates.TemplateResponse("logs.html", {"request": request, "posts": posts})

@app.post("/publish")
async def publish(request: Request):
    data = await request.json()
    platform = data.get("platform")
    message = data.get("message")
    media_url = data.get("media_url")

    session = SessionLocal()
    token = session.query(Token).filter(Token.platform == platform).first()
    if not token:
        session.close()
        raise HTTPException(status_code=404, detail="No connected account found for this platform")

    print(f"[PUBLISH] {platform}: {message}")
    post = Post(platform=platform, account_id=token.account_id, message=message, media_url=media_url)
    session.add(post)
    session.commit()
    session.close()
    return JSONResponse({"status": "success", "platform": platform, "message": message})

# ----------------------
# 🔹 ADD THESE AT THE END
# ----------------------

# Register each router from /auth/
app.include_router(facebook.router)
app.include_router(instagram.router)
app.include_router(linkedin.router)
app.include_router(twitter.router)
app.include_router(tiktok.router)
app.include_router(youtube.router)
app.include_router(pinterest.router)
app.include_router(bluesky.router)
