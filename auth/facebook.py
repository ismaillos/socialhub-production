import requests, datetime
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from db.database import SessionLocal
from db.models import Token
from core.config import get_secret
router=APIRouter(prefix='/auth/facebook', tags=['Facebook'])
templates=Jinja2Templates(directory='templates')
SCOPE='pages_show_list,pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish,business_management'
def _missing(keys, hint='/settings'):
    return HTMLResponse('<h3>Missing Facebook settings</h3><ul>'+''.join(f'<li>{k}</li>' for k in keys)+f'</ul><a href="{hint}">Open settings</a>',400)
@router.get('/login')
def login():
    cid=get_secret('FACEBOOK_CLIENT_ID'); red=get_secret('FACEBOOK_REDIRECT_URI')
    if not cid or not red: return _missing(['FACEBOOK_CLIENT_ID','FACEBOOK_REDIRECT_URI'])
    url=f'https://www.facebook.com/v19.0/dialog/oauth?client_id={cid}&redirect_uri={red}&scope={SCOPE}&response_type=code'
    return RedirectResponse(url)
@router.get('/callback', response_class=HTMLResponse)
def callback(request:Request, code:str|None=None, error:str|None=None):
    if error: return HTMLResponse(f'<pre>{error}</pre>',400)
    cid=get_secret('FACEBOOK_CLIENT_ID'); cs=get_secret('FACEBOOK_CLIENT_SECRET'); red=get_secret('FACEBOOK_REDIRECT_URI')
    if not cid or not cs or not red: return _missing(['FACEBOOK_CLIENT_ID','FACEBOOK_CLIENT_SECRET','FACEBOOK_REDIRECT_URI'])
    tr=requests.get('https://graph.facebook.com/v19.0/oauth/access_token', params={'client_id':cid,'redirect_uri':red,'client_secret':cs,'code':code}, timeout=20).json()
    at=tr.get('access_token'); ei=tr.get('expires_in')
    if not at: return HTMLResponse(f'<pre>{tr}</pre>',400)
    pages=requests.get('https://graph.facebook.com/me/accounts', params={'access_token':at}, timeout=20).json().get('data',[])
    if not pages: return RedirectResponse('/accounts')
    if len(pages)==1:
        p=pages[0]; pg=requests.get(f'https://graph.facebook.com/{p["id"]}', params={'fields':'name,access_token','access_token':at}, timeout=20).json()
        page_name=pg.get('name') or p['id']; page_token=pg.get('access_token') or p.get('access_token')
        with SessionLocal() as s:
            ex=s.query(Token).filter(Token.platform=='facebook', Token.account_id==p['id']).first()
            if ex: ex.username=page_name; ex.page_access_token=page_token; ex.access_token=at; 
            else: s.add(Token(platform='facebook', account_id=p['id'], username=page_name, page_id=p['id'], page_access_token=page_token, access_token=at))
            if ei and ex: ex.expires_at=datetime.datetime.utcnow()+datetime.timedelta(seconds=int(ei))
            s.commit()
        return RedirectResponse('/accounts')
    return templates.TemplateResponse('select_pages.html', {'request':request,'pages':pages,'user_token':at})
@router.post('/select-multi')
def select_multi(page_ids:list[str]=Form(...), user_token:str=Form(...)):
    for pid in page_ids:
        pg=requests.get(f'https://graph.facebook.com/{pid}', params={'fields':'name,access_token','access_token':user_token}, timeout=20).json()
        name=pg.get('name') or pid; page_token=pg.get('access_token')
        with SessionLocal() as s:
            ex=s.query(Token).filter(Token.platform=='facebook', Token.account_id==pid).first()
            if ex: ex.username=name; ex.page_access_token=page_token; ex.access_token=user_token
            else: s.add(Token(platform='facebook', account_id=pid, username=name, page_id=pid, page_access_token=page_token, access_token=user_token))
            s.commit()
    return RedirectResponse('/accounts')
