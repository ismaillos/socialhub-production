import requests, datetime
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
from db.database import SessionLocal
from db.models import Token
from core.providers import get_provider_secrets

router = APIRouter(prefix='/auth/tiktok', tags=['TikTok'])
SCOPE = 'user.info.basic,video.upload'
STATE = 'secure_state_12345'

def _missing(keys, redirect_hint='/settings'):
    missing_list = ''.join(f'<li>{k}</li>' for k in keys)
    return HTMLResponse(f"""
        <h3>Missing TikTok OAuth settings</h3>
        <p>Add keys in <a href='{redirect_hint}'>/settings</a> or env:</p>
        <ul>{missing_list}</ul>
        <pre>TIKTOK_CLIENT_KEY\nTIKTOK_CLIENT_SECRET\nTIKTOK_REDIRECT_URI</pre>
    """, status_code=400)

@router.get('/login')
def tiktok_login(client_key: str | None = None, redirect_uri: str | None = None):
    cfg, _ = get_provider_secrets(['TIKTOK_CLIENT_KEY','TIKTOK_CLIENT_SECRET','TIKTOK_REDIRECT_URI'])
    if client_key: cfg['TIKTOK_CLIENT_KEY'] = client_key
    if redirect_uri: cfg['TIKTOK_REDIRECT_URI'] = redirect_uri
    missing = [k for k in ['TIKTOK_CLIENT_KEY','TIKTOK_REDIRECT_URI'] if not cfg.get(k)]
    if missing: return _missing(missing)
    url = ('https://www.tiktok.com/v2/auth/authorize/'
           f'?client_key={cfg["TIKTOK_CLIENT_KEY"]}&scope={SCOPE}&response_type=code'
           f'&redirect_uri={cfg["TIKTOK_REDIRECT_URI"]}&state={STATE}')
    return RedirectResponse(url=url)

@router.get('/callback')
def tiktok_callback(code: str | None = None, state: str | None = None, error: str | None = None):
    if error:
        return HTMLResponse(f'<p>OAuth Error: {error}</p>', status_code=400)
    cfg, missing = get_provider_secrets(['TIKTOK_CLIENT_KEY','TIKTOK_CLIENT_SECRET','TIKTOK_REDIRECT_URI'])
    if missing: return _missing(missing)
    data = {'client_key': cfg['TIKTOK_CLIENT_KEY'],'client_secret': cfg['TIKTOK_CLIENT_SECRET'],
            'code': code,'grant_type': 'authorization_code','redirect_uri': cfg['TIKTOK_REDIRECT_URI']}
    res = requests.post('https://open-api.tiktok.com/oauth/access_token/', data=data, timeout=20).json()
    if not (res.get('data') and res['data'].get('access_token')):
        return HTMLResponse(f'<pre>{res}</pre>', status_code=400)
    at = res['data']['access_token']; rt = res['data'].get('refresh_token'); open_id = res['data'].get('open_id')
    expires_in = res['data'].get('expires_in')
    headers = {'Authorization': f'Bearer {at}'}
    me = requests.get('https://open-api.tiktok.com/user/info/', headers=headers, timeout=20).json()
    username = None
    if me.get('data') and me['data'].get('user'):
        username = me['data']['user'].get('display_name')
    with SessionLocal() as s:
        existing = s.query(Token).filter(Token.platform=='tiktok', Token.account_id==open_id).first()
        if existing:
            existing.username = username; existing.access_token = at; existing.refresh_token = rt
            if expires_in: existing.expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(expires_in))
        else:
            s.add(Token(platform='tiktok', account_id=open_id or 'unknown', username=username,
                        access_token=at, refresh_token=rt,
                        expires_at=(datetime.datetime.utcnow()+datetime.timedelta(seconds=int(expires_in))) if expires_in else None))
        s.commit()
    return RedirectResponse(url='/accounts')
