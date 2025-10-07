import requests, datetime
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
from db.database import SessionLocal
from db.models import Token
from core.providers import get_provider_secrets

router = APIRouter(prefix='/auth/youtube', tags=['YouTube'])
SCOPE = 'https://www.googleapis.com/auth/youtube.readonly openid email'

def _missing(keys, redirect_hint='/settings'):
    missing_list = ''.join(f'<li>{k}</li>' for k in keys)
    return HTMLResponse(f"""
        <h3>Missing Google OAuth settings</h3>
        <p>Add keys in <a href='{redirect_hint}'>/settings</a> or env:</p>
        <ul>{missing_list}</ul>
        <pre>GOOGLE_CLIENT_ID\nGOOGLE_CLIENT_SECRET\nGOOGLE_REDIRECT_URI</pre>
    """, status_code=400)

@router.get('/login')
def yt_login(client_id: str | None = None, redirect_uri: str | None = None):
    cfg, _ = get_provider_secrets(['GOOGLE_CLIENT_ID','GOOGLE_CLIENT_SECRET','GOOGLE_REDIRECT_URI'])
    if client_id: cfg['GOOGLE_CLIENT_ID'] = client_id
    if redirect_uri: cfg['GOOGLE_REDIRECT_URI'] = redirect_uri
    missing = [k for k in ['GOOGLE_CLIENT_ID','GOOGLE_REDIRECT_URI'] if not cfg.get(k)]
    if missing: return _missing(missing)
    auth_url = ('https://accounts.google.com/o/oauth2/v2/auth'
        f'?client_id={cfg["GOOGLE_CLIENT_ID"]}&redirect_uri={cfg["GOOGLE_REDIRECT_URI"]}'
        f'&response_type=code&access_type=offline&prompt=consent&scope={SCOPE}')
    return RedirectResponse(url=auth_url)

@router.get('/callback')
def yt_callback(code: str | None = None, error: str | None = None):
    if error:
        return HTMLResponse(f'<p>OAuth Error: {error}</p>', status_code=400)
    cfg, missing = get_provider_secrets(['GOOGLE_CLIENT_ID','GOOGLE_CLIENT_SECRET','GOOGLE_REDIRECT_URI'])
    if missing: return _missing(missing)
    data = {'code': code,'client_id': cfg['GOOGLE_CLIENT_ID'],'client_secret': cfg['GOOGLE_CLIENT_SECRET'],
            'redirect_uri': cfg['GOOGLE_REDIRECT_URI'],'grant_type': 'authorization_code'}
    token_res = requests.post('https://oauth2.googleapis.com/token', data=data, timeout=20).json()
    access_token = token_res.get('access_token'); refresh_token = token_res.get('refresh_token')
    expires_in = token_res.get('expires_in')
    if not access_token:
        return HTMLResponse(f'<pre>{token_res}</pre>', status_code=400)
    ch = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true',
                       headers={'Authorization': f'Bearer {access_token}'}, timeout=20).json()
    channel_id = channel_title = None
    if ch.get('items'):
        channel_id = ch['items'][0]['id']; channel_title = ch['items'][0]['snippet']['title']
    with SessionLocal() as s:
        existing = s.query(Token).filter(Token.platform=='youtube', Token.account_id==channel_id).first()
        if existing:
            existing.username = channel_title; existing.access_token = access_token; existing.refresh_token = refresh_token
            if expires_in: existing.expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(expires_in))
        else:
            s.add(Token(platform='youtube', account_id=channel_id or 'unknown', username=channel_title,
                        access_token=access_token, refresh_token=refresh_token,
                        expires_at=(datetime.datetime.utcnow()+datetime.timedelta(seconds=int(expires_in))) if expires_in else None))
        s.commit()
    return RedirectResponse(url='/accounts')
