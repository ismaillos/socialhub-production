import requests, datetime
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
from db.database import SessionLocal
from db.models import Token
from core.config import get_secret
router=APIRouter(prefix='/auth/tiktok', tags=['TikTok'])
SCOPE='user.info.basic,video.upload'; STATE='state123'
def _missing(keys, hint='/settings'):
    return HTMLResponse('<h3>Missing TikTok settings</h3><ul>'+''.join(f'<li>{k}</li>' for k in keys)+f'</ul><a href="{hint}">Open settings</a>',400)
@router.get('/login')
def login():
    ck=get_secret('TIKTOK_CLIENT_KEY'); red=get_secret('TIKTOK_REDIRECT_URI')
    if not ck or not red: return _missing(['TIKTOK_CLIENT_KEY','TIKTOK_REDIRECT_URI'])
    url=f'https://www.tiktok.com/v2/auth/authorize/?client_key={ck}&scope={SCOPE}&response_type=code&redirect_uri={red}&state={STATE}'
    return RedirectResponse(url)
@router.get('/callback')
def callback(code:str|None=None, state:str|None=None, error:str|None=None):
    if error: return HTMLResponse(f'<pre>{error}</pre>',400)
    ck=get_secret('TIKTOK_CLIENT_KEY'); cs=get_secret('TIKTOK_CLIENT_SECRET'); red=get_secret('TIKTOK_REDIRECT_URI')
    if not ck or not cs or not red: return _missing(['TIKTOK_CLIENT_KEY','TIKTOK_CLIENT_SECRET','TIKTOK_REDIRECT_URI'])
    data={'client_key':ck,'client_secret':cs,'code':code,'grant_type':'authorization_code','redirect_uri':red}
    res=requests.post('https://open-api.tiktok.com/oauth/access_token/', data=data, timeout=20).json()
    d=res.get('data',{}); at=d.get('access_token'); rt=d.get('refresh_token'); open_id=d.get('open_id'); ei=d.get('expires_in')
    if not at: return HTMLResponse(f'<pre>{res}</pre>',400)
    headers={'Authorization':f'Bearer {at}'}
    me=requests.get('https://open-api.tiktok.com/user/info/', headers=headers, timeout=20).json()
    username=None
    if me.get('data') and me['data'].get('user'): username=me['data']['user'].get('display_name')
    with SessionLocal() as s:
        ex=s.query(Token).filter(Token.platform=='tiktok', Token.account_id==(open_id or 'unknown')).first()
        if ex: ex.username=username; ex.access_token=at; ex.refresh_token=rt
        else: s.add(Token(platform='tiktok', account_id=open_id or 'unknown', username=username, access_token=at, refresh_token=rt))
        if ei and ex: ex.expires_at=datetime.datetime.utcnow()+datetime.timedelta(seconds=int(ei))
        s.commit()
    return RedirectResponse('/accounts')
