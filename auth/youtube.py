import requests, datetime
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
from db.database import SessionLocal
from db.models import Token
from core.config import get_secret
router=APIRouter(prefix='/auth/youtube', tags=['YouTube'])
SCOPE='https://www.googleapis.com/auth/youtube.upload openid email'
def _missing(keys, hint='/settings'):
    return HTMLResponse('<h3>Missing Google settings</h3><ul>'+''.join(f'<li>{k}</li>' for k in keys)+f'</ul><a href="{hint}">Open settings</a>',400)
@router.get('/login')
def login():
    cid=get_secret('GOOGLE_CLIENT_ID'); red=get_secret('GOOGLE_REDIRECT_URI')
    if not cid or not red: return _missing(['GOOGLE_CLIENT_ID','GOOGLE_REDIRECT_URI'])
    url=('https://accounts.google.com/o/oauth2/v2/auth'
         f'?client_id={cid}&redirect_uri={red}&response_type=code&access_type=offline&prompt=consent&scope={SCOPE}')
    return RedirectResponse(url)
@router.get('/callback')
def callback(code:str|None=None, error:str|None=None):
    if error: return HTMLResponse(f'<pre>{error}</pre>',400)
    cid=get_secret('GOOGLE_CLIENT_ID'); cs=get_secret('GOOGLE_CLIENT_SECRET'); red=get_secret('GOOGLE_REDIRECT_URI')
    if not cid or not cs or not red: return _missing(['GOOGLE_CLIENT_ID','GOOGLE_CLIENT_SECRET','GOOGLE_REDIRECT_URI'])
    data={'code':code,'client_id':cid,'client_secret':cs,'redirect_uri':red,'grant_type':'authorization_code'}
    tr=requests.post('https://oauth2.googleapis.com/token', data=data, timeout=20).json()
    at=tr.get('access_token'); rt=tr.get('refresh_token'); ei=tr.get('expires_in')
    if not at: return HTMLResponse(f'<pre>{tr}</pre>',400)
    ch=requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true', headers={'Authorization':f'Bearer {at}'}, timeout=20).json()
    ch_id=ch_title=None
    if ch.get('items'): ch_id=ch['items'][0]['id']; ch_title=ch['items'][0]['snippet']['title']
    with SessionLocal() as s:
        ex=s.query(Token).filter(Token.platform=='youtube', Token.account_id==(ch_id or 'unknown')).first()
        if ex: ex.username=ch_title; ex.access_token=at; ex.refresh_token=rt
        else: s.add(Token(platform='youtube', account_id=ch_id or 'unknown', username=ch_title, access_token=at, refresh_token=rt))
        if ei and ex: ex.expires_at=datetime.datetime.utcnow()+datetime.timedelta(seconds=int(ei))
        s.commit()
    return RedirectResponse('/accounts')
