import requests, datetime
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
from db.database import SessionLocal
from db.models import Token
from core.config import get_secret
router=APIRouter(prefix='/auth/instagram', tags=['Instagram'])
SCOPE='instagram_basic,instagram_content_publish,pages_show_list,business_management'
def _missing(keys, hint='/settings'):
    return HTMLResponse('<h3>Missing Instagram settings</h3><ul>'+''.join(f'<li>{k}</li>' for k in keys)+f'</ul><a href="{hint}">Open settings</a>',400)
@router.get('/login')
def login():
    cid=get_secret('FACEBOOK_CLIENT_ID'); red=get_secret('INSTAGRAM_REDIRECT_URI')
    if not cid or not red: return _missing(['FACEBOOK_CLIENT_ID','INSTAGRAM_REDIRECT_URI'])
    url=f'https://www.facebook.com/v19.0/dialog/oauth?client_id={cid}&redirect_uri={red}&scope={SCOPE}&response_type=code'
    return RedirectResponse(url)
@router.get('/callback')
def callback(code:str|None=None, error:str|None=None):
    if error: return HTMLResponse(f'<pre>{error}</pre>',400)
    cid=get_secret('FACEBOOK_CLIENT_ID'); cs=get_secret('FACEBOOK_CLIENT_SECRET'); red=get_secret('INSTAGRAM_REDIRECT_URI')
    if not cid or not cs or not red: return _missing(['FACEBOOK_CLIENT_ID','FACEBOOK_CLIENT_SECRET','INSTAGRAM_REDIRECT_URI'])
    tr=requests.get('https://graph.facebook.com/v19.0/oauth/access_token', params={'client_id':cid,'redirect_uri':red,'client_secret':cs,'code':code}, timeout=20).json()
    at=tr.get('access_token'); ei=tr.get('expires_in')
    if not at: return HTMLResponse(f'<pre>{tr}</pre>',400)
    pages=requests.get('https://graph.facebook.com/me/accounts', params={'access_token':at}, timeout=20).json().get('data',[])
    with SessionLocal() as s:
        for p in pages:
            pid=p['id']
            detail=requests.get(f'https://graph.facebook.com/{pid}', params={'fields':'instagram_business_account,access_token,name','access_token':at}, timeout=20).json()
            ig=detail.get('instagram_business_account'); page_token=detail.get('access_token') or p.get('access_token')
            if not ig or not ig.get('id'): continue
            ig_id=ig['id']
            prof=requests.get(f'https://graph.facebook.com/{ig_id}', params={'fields':'username,profile_picture_url','access_token':page_token}, timeout=20).json()
            uname=prof.get('username'); pic=prof.get('profile_picture_url')
            ex=s.query(Token).filter(Token.platform=='instagram', Token.account_id==ig_id).first()
            if ex: ex.username=uname; ex.profile_pic=pic; ex.business_id=ig_id; ex.page_id=pid; ex.page_access_token=page_token; ex.access_token=at
            else: s.add(Token(platform='instagram', account_id=ig_id, username=uname, profile_pic=pic, business_id=ig_id, page_id=pid, page_access_token=page_token, access_token=at))
            if ei and ex: ex.expires_at=datetime.datetime.utcnow()+datetime.timedelta(seconds=int(ei))
        s.commit()
    return RedirectResponse('/accounts')
