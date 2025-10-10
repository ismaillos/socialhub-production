
from fastapi import FastAPI
from routers import posts, users, auth
from sqlmodel import SQLModel
from models.user_settings import UserSettings
from config import settings
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(settings.engine)

app.include_router(users.router, tags=["Dashboard"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
