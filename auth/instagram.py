import requests, datetime
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
from db.database import SessionLocal
from db.models import Token
from core.providers import get_provider_secrets

router = APIRouter(prefix='/auth/instagram', tags=['Instagram'])
SCOPE = 'instagram_basic,instagram_content_publish,pages_show_list,business_management'

def _missing(keys, redirect_hint='/settings'):
    missing_list = ''.join(f'<li>{k}</li>' for k in keys)
    return HTMLResponse(f"""
        <h3>Missing Instagram OAuth settings</h3>
        <p>Add keys in <a href='{redirect_hint}'>/settings</a> or env:</p>
        <ul>{missing_list}</ul>
        <pre>FACEBOOK_CLIENT_ID\nFACEBOOK_CLIENT_SECRET\nINSTAGRAM_REDIRECT_URI</pre>
    """, status_code=400)

@router.get('/login')
def ig_login(client_id: str | None = None, redirect_uri: str | None = None):
    cfg, _ = get_provider_secrets(['FACEBOOK_CLIENT_ID','FACEBOOK_CLIENT_SECRET','INSTAGRAM_REDIRECT_URI'])
    if client_id: cfg['FACEBOOK_CLIENT_ID'] = client_id
    if redirect_uri: cfg['INSTAGRAM_REDIRECT_URI'] = redirect_uri
    missing = [k for k in ['FACEBOOK_CLIENT_ID','INSTAGRAM_REDIRECT_URI'] if not cfg.get(k)]
    if missing: return _missing(missing)
    url = ('https://www.facebook.com/v19.0/dialog/oauth'
           f'?client_id={cfg["FACEBOOK_CLIENT_ID"]}'
           f'&redirect_uri={cfg["INSTAGRAM_REDIRECT_URI"]}'
           f'&scope={SCOPE}&response_type=code')
    return RedirectResponse(url=url)

@router.get('/callback')
def ig_callback(code: str | None = None, error: str | None = None):
    if error:
        return HTMLResponse(f'<p>OAuth Error: {error}</p>', status_code=400)
    cfg, missing = get_provider_secrets(['FACEBOOK_CLIENT_ID','FACEBOOK_CLIENT_SECRET','INSTAGRAM_REDIRECT_URI'])
    if missing: return _missing(missing)
    token_res = requests.get('https://graph.facebook.com/v19.0/oauth/access_token', params={
        'client_id': cfg['FACEBOOK_CLIENT_ID'],
        'redirect_uri': cfg['INSTAGRAM_REDIRECT_URI'],
        'client_secret': cfg['FACEBOOK_CLIENT_SECRET'],
        'code': code
    }, timeout=20).json()
    user_access_token = token_res.get('access_token'); expires_in = token_res.get('expires_in')
    if not user_access_token:
        return HTMLResponse(f'<pre>{token_res}</pre>', status_code=400)
    pages = requests.get('https://graph.facebook.com/me/accounts',
                         params={'access_token': user_access_token}, timeout=20).json().get('data', [])
    with SessionLocal() as s:
        for p in pages:
            pid = p['id']
            detail = requests.get(f'https://graph.facebook.com/{pid}', params={
                'fields':'instagram_business_account,access_token,name',
                'access_token': user_access_token
            }, timeout=20).json()
            ig_obj = detail.get('instagram_business_account')
            page_token = detail.get('access_token') or p.get('access_token')
            if not ig_obj or not ig_obj.get('id'):
                continue
            ig_id = ig_obj['id']
            ig_profile = requests.get(f'https://graph.facebook.com/{ig_id}', params={
                'fields':'username,profile_picture_url',
                'access_token': page_token
            }, timeout=20).json()
            ig_username = ig_profile.get('username')
            profile_pic = ig_profile.get('profile_picture_url')
            existing = s.query(Token).filter(Token.platform=='instagram', Token.account_id==ig_id).first()
            if existing:
                existing.username = ig_username; existing.profile_pic = profile_pic
                existing.business_id = ig_id; existing.page_id = pid
                existing.page_access_token = page_token; existing.access_token = user_access_token
                if expires_in: existing.expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(expires_in))
            else:
                s.add(Token(platform='instagram', account_id=ig_id, username=ig_username, profile_pic=profile_pic,
                            business_id=ig_id, page_id=pid, page_access_token=page_token, access_token=user_access_token,
                            expires_at=(datetime.datetime.utcnow()+datetime.timedelta(seconds=int(expires_in))) if expires_in else None))
        s.commit()
    return RedirectResponse(url='/accounts')
