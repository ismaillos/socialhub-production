import os, requests
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from db.database import SessionLocal
from db.models import Token
router = APIRouter(prefix="/auth/facebook", tags=["Facebook"])
templates = Jinja2Templates(directory="templates")
CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("FACEBOOK_REDIRECT_URI", "https://socialhub-production-production.up.railway.app/auth/facebook/callback")
SCOPE = "pages_show_list,pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish,business_management"
@router.get("/login")
def fb_login():
    auth_url = ("https://www.facebook.com/v19.0/dialog/oauth"
        f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE}&response_type=code")
    return RedirectResponse(url=auth_url)
@router.get("/callback", response_class=HTMLResponse)
def fb_callback(request: Request, code: str = None, error: str = None):
    if error: return JSONResponse({"status":"error","message":error}, status_code=400)
    token_params = {"client_id": CLIENT_ID,"redirect_uri": REDIRECT_URI,"client_secret": CLIENT_SECRET,"code": code}
    token_res = requests.get("https://graph.facebook.com/v19.0/oauth/access_token", params=token_params).json()
    user_access_token = token_res.get("access_token")
    if not user_access_token: return JSONResponse({"status":"error","details": token_res}, status_code=400)
    pages = requests.get("https://graph.facebook.com/me/accounts", params={"access_token": user_access_token}).json()
    page_list = pages.get("data", [])
    if len(page_list) <= 1:
        page_id = page_list[0]["id"] if page_list else None
        page_token = page_list[0].get("access_token") if page_list else None
        me = requests.get("https://graph.facebook.com/me", params={"access_token": user_access_token, "fields": "id,name"}).json()
        with SessionLocal() as session:
            existing = session.query(Token).filter(Token.platform=="facebook").first() or Token(platform="facebook")
            existing.account_id = me.get("id")
            existing.username = me.get("name")
            existing.access_token = user_access_token
            existing.page_id = page_id
            existing.page_access_token = page_token
            session.add(existing); session.commit()
        return RedirectResponse(url="/accounts")
    else:
        return templates.TemplateResponse("select_page.html", {"request": request, "pages": page_list, "user_token": user_access_token})
@router.post("/select")
def fb_select(page_id: str = Form(...), user_token: str = Form(...) ):
    me = requests.get("https://graph.facebook.com/me", params={"access_token": user_token, "fields": "id,name"}).json()
    pg = requests.get(f"https://graph.facebook.com/{page_id}", params={"fields":"access_token", "access_token": user_token}).json()
    page_token = pg.get("access_token")
    with SessionLocal() as session:
        existing = session.query(Token).filter(Token.platform=="facebook").first() or Token(platform="facebook")
        existing.account_id = me.get("id")
        existing.username = me.get("name")
        existing.access_token = user_token
        existing.page_id = page_id
        existing.page_access_token = page_token
        session.add(existing); session.commit()
    return RedirectResponse(url="/accounts")
