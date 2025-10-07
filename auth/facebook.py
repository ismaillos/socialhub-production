import requests, datetime
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from db.database import SessionLocal
from db.models import Token
from core.providers import get_provider_secrets

router = APIRouter(prefix='/auth/facebook', tags=['Facebook'])
templates = Jinja2Templates(directory='templates')
SCOPE = ('pages_show_list,pages_read_engagement,pages_manage_posts,'
         'instagram_basic,instagram_content_publish,business_management')

def _missing(keys, redirect_hint='/settings'):
    missing_list = ''.join(f'<li>{k}</li>' for k in keys)
    return HTMLResponse(f"""
        <h3>Missing Facebook OAuth settings</h3>
        <p>Add keys in <a href='{redirect_hint}'>/settings</a> or env:</p>
        <ul>{missing_list}</ul>
        <pre>FACEBOOK_CLIENT_ID\nFACEBOOK_CLIENT_SECRET\nFACEBOOK_REDIRECT_URI</pre>
    """, status_code=400)

@router.get('/login')
def fb_login(client_id: str | None = None, redirect_uri: str | None = None):
    cfg, _ = get_provider_secrets(['FACEBOOK_CLIENT_ID','FACEBOOK_CLIENT_SECRET','FACEBOOK_REDIRECT_URI'])
    if client_id: cfg['FACEBOOK_CLIENT_ID'] = client_id
    if redirect_uri: cfg['FACEBOOK_REDIRECT_URI'] = redirect_uri
    missing = [k for k in ['FACEBOOK_CLIENT_ID','FACEBOOK_REDIRECT_URI'] if not cfg.get(k)]
    if missing: return _missing(missing)
    url = ('https://www.facebook.com/v19.0/dialog/oauth'
           f'?client_id={cfg["FACEBOOK_CLIENT_ID"]}'
           f'&redirect_uri={cfg["FACEBOOK_REDIRECT_URI"]}'
           f'&scope={SCOPE}&response_type=code')
    return RedirectResponse(url=url)

@router.get('/callback', response_class=HTMLResponse)
def fb_callback(request: Request, code: str | None = None, error: str | None = None):
    if error:
        return HTMLResponse(f'<p>OAuth Error: {error}</p>', status_code=400)
    cfg, missing = get_provider_secrets(['FACEBOOK_CLIENT_ID','FACEBOOK_CLIENT_SECRET','FACEBOOK_REDIRECT_URI'])
    if missing: return _missing(missing)
    token_res = requests.get('https://graph.facebook.com/v19.0/oauth/access_token', params={
        'client_id': cfg['FACEBOOK_CLIENT_ID'],
        'redirect_uri': cfg['FACEBOOK_REDIRECT_URI'],
        'client_secret': cfg['FACEBOOK_CLIENT_SECRET'],
        'code': code
    }, timeout=20).json()
    user_access_token = token_res.get('access_token')
    expires_in = token_res.get('expires_in')
    if not user_access_token:
        return HTMLResponse(f'<pre>{token_res}</pre>', status_code=400)
    pages = requests.get('https://graph.facebook.com/me/accounts',
                         params={'access_token': user_access_token}, timeout=20).json().get('data', [])
    if not pages:
        return RedirectResponse(url='/accounts')
    if len(pages) == 1:
        p = pages[0]
        pg = requests.get(f'https://graph.facebook.com/{p["id"]}', params={
            'fields':'name,access_token','access_token': user_access_token
        }, timeout=20).json()
        page_name = pg.get('name') or p['id']
        page_token = pg.get('access_token') or p.get('access_token')
        with SessionLocal() as s:
            existing = s.query(Token).filter(Token.platform=='facebook', Token.account_id==p['id']).first()
            if existing:
                existing.username = page_name; existing.page_access_token = page_token; existing.access_token = user_access_token
                if expires_in: existing.expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(expires_in))
            else:
                s.add(Token(platform='facebook', account_id=p['id'], username=page_name,
                            page_id=p['id'], page_access_token=page_token, access_token=user_access_token,
                            expires_at=(datetime.datetime.utcnow()+datetime.timedelta(seconds=int(expires_in))) if expires_in else None))
            s.commit()
        return RedirectResponse(url='/accounts')
    return templates.TemplateResponse('select_pages.html', {'request': request, 'pages': pages, 'user_token': user_access_token})

@router.post('/select-multi')
def fb_select_multi(page_ids: list[str] = Form(...), user_token: str = Form(...)):
    for pid in page_ids:
        pg = requests.get(f'https://graph.facebook.com/{pid}', params={
            'fields':'name,access_token','access_token': user_token
        }, timeout=20).json()
        page_name = pg.get('name') or pid
        page_token = pg.get('access_token')
        with SessionLocal() as s:
            existing = s.query(Token).filter(Token.platform=='facebook', Token.account_id==pid).first()
            if existing:
                existing.username = page_name; existing.page_access_token = page_token; existing.access_token = user_token
            else:
                s.add(Token(platform='facebook', account_id=pid, username=page_name,
                            page_id=pid, page_access_token=page_token, access_token=user_token))
            s.commit()
    return RedirectResponse(url='/accounts')
