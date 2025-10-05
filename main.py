import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from db.database import Base, engine, SessionLocal
from db.models import Token, Post
from auth import facebook, instagram, tiktok, youtube

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SocialHub 4-Platform", version="1.0.0")

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
        token = session.query(Token).filter(Token.platform == platform).first()
        if not token:
            raise HTTPException(status_code=404, detail=f"No account for {platform}")
        session.delete(token)
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
        post = Post(platform=platform, account_id=token.account_id, message=message, media_url=media_url)
        session.add(post)
        session.commit()

    return JSONResponse({"status": "ok", "platform": platform, "message": message})

@app.get("/health")
def health():
    return {"status": "ok", "uptime": datetime.datetime.utcnow().isoformat()}

app.include_router(facebook.router)
app.include_router(instagram.router)
app.include_router(tiktok.router)
app.include_router(youtube.router)
