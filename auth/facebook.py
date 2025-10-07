import requests
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from db.database import SessionLocal
from db.models import Token
from core.config import get_secret

router = APIRouter(prefix="/auth/facebook", tags=["Facebook"])
templates = Jinja2Templates(directory="templates")

CLIENT_ID = get_secret("FACEBOOK_CLIENT_ID", "")
CLIENT_SECRET = get_secret("FACEBOOK_CLIENT_SECRET", "")
REDIRECT_URI = get_secret("FACEBOOK_REDIRECT_URI", "")
SCOPE = "pages_show_list,pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish,business_management"

@router.get("/login")
def fb_login():
    url = ("https://www.facebook.com/v19.0/dialog/oauth"
           f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
           f"&scope={SCOPE}&response_type=code")
    return RedirectResponse(url=url)

@router.get("/callback", response_class=HTMLResponse)
def fb_callback(request: Request, code: str = None, error: str = None):
    if error:
        return JSONResponse({"status":"error","message":error}, status_code=400)
    token_res = requests.get("https://graph.facebook.com/v19.0/oauth/access_token",
                             params={"client_id": CLIENT_ID, "redirect_uri": REDIRECT_URI,
                                     "client_secret": CLIENT_SECRET, "code": code}).json()
    user_access_token = token_res.get("access_token")
    if not user_access_token:
        return JSONResponse({"status":"error","details": token_res}, status_code=400)
    pages = requests.get("https://graph.facebook.com/me/accounts",
                         params={"access_token": user_access_token}).json().get("data", [])
    if not pages:
        return RedirectResponse(url="/accounts")
    if len(pages) == 1:
        p = pages[0]
        pg = requests.get(f"https://graph.facebook.com/{p['id']}",
                          params={"fields":"name,access_token","access_token": user_access_token}).json()
        page_name = pg.get("name") or p["id"]
        page_token = pg.get("access_token") or p.get("access_token")
        with SessionLocal() as s:
            existing = s.query(Token).filter(Token.platform=="facebook", Token.account_id==p["id"]).first()
            if existing:
                existing.username = page_name; existing.page_access_token = page_token; existing.access_token = user_access_token
            else:
                s.add(Token(platform="facebook", account_id=p["id"], username=page_name,
                            page_id=p["id"], page_access_token=page_token, access_token=user_access_token))
            s.commit()
        return RedirectResponse(url="/accounts")
    return templates.TemplateResponse("select_pages.html", {"request": request, "pages": pages, "user_token": user_access_token})

@router.post("/select-multi")
def fb_select_multi(page_ids: list[str] = Form(...), user_token: str = Form(...)):
    for pid in page_ids:
        pg = requests.get(f"https://graph.facebook.com/{pid}",
                          params={"fields":"name,access_token","access_token": user_token}).json()
        page_name = pg.get("name") or pid
        page_token = pg.get("access_token")
        with SessionLocal() as s:
            existing = s.query(Token).filter(Token.platform=="facebook", Token.account_id==pid).first()
            if existing:
                existing.username = page_name; existing.page_access_token = page_token; existing.access_token = user_token
            else:
                s.add(Token(platform="facebook", account_id=pid, username=page_name,
                            page_id=pid, page_access_token=page_token, access_token=user_token))
            s.commit()
    return RedirectResponse(url="/accounts")
