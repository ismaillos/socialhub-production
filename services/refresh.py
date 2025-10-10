import datetime, requests
from typing import Dict, Any
from db.database import SessionLocal
from db.models import Token
from core.config import get_secret
def _now(): return datetime.datetime.utcnow()
def refresh_facebook_and_instagram()->Dict[str,Any]:
    cid=get_secret('FACEBOOK_CLIENT_ID',''); cs=get_secret('FACEBOOK_CLIENT_SECRET','')
    if not cid or not cs: return {'status':'skipped','missing':['FACEBOOK_CLIENT_ID','FACEBOOK_CLIENT_SECRET']}
    changed=0; pages_updated=0
    with SessionLocal() as s:
        rows=s.query(Token).filter(Token.platform.in_(['facebook','instagram'])).all()
        for r in rows:
            if r.access_token:
                try:
                    res=requests.get('https://graph.facebook.com/v19.0/oauth/access_token',params={
                        'grant_type':'fb_exchange_token','client_id':cid,'client_secret':cs,'fb_exchange_token':r.access_token
                    },timeout=20).json()
                    t=res.get('access_token'); ei=res.get('expires_in')
                    if t: r.access_token=t; changed+=1
                    if ei: r.expires_at=_now()+datetime.timedelta(seconds=int(ei))
                except Exception: pass
            if r.page_id and r.access_token:
                try:
                    pg=requests.get(f'https://graph.facebook.com/{r.page_id}',params={'fields':'name,access_token','access_token':r.access_token},timeout=20).json()
                    pt=pg.get('access_token')
                    if pt: r.page_access_token=pt; pages_updated+=1
                except Exception: pass
        s.commit()
    return {'status':'ok','user_tokens_refreshed':changed,'page_tokens_updated':pages_updated}
def refresh_tiktok()->Dict[str,Any]:
    ck=get_secret('TIKTOK_CLIENT_KEY',''); cs=get_secret('TIKTOK_CLIENT_SECRET','')
    if not ck or not cs: return {'status':'skipped','missing':['TIKTOK_CLIENT_KEY','TIKTOK_CLIENT_SECRET']}
    changed=0
    with SessionLocal() as s:
        rows=s.query(Token).filter(Token.platform=='tiktok').all()
        for r in rows:
            if not r.refresh_token: continue
            try:
                res=requests.post('https://open-api.tiktok.com/oauth/refresh_token/',data={
                    'client_key':ck,'grant_type':'refresh_token','refresh_token':r.refresh_token
                },timeout=20).json()
                d=res.get('data',{})
                if d.get('access_token'):
                    r.access_token=d['access_token']; r.refresh_token=d.get('refresh_token',r.refresh_token)
                    ei=d.get('expires_in'); 
                    if ei: r.expires_at=_now()+datetime.timedelta(seconds=int(ei))
                    changed+=1
            except Exception: pass
        s.commit()
    return {'status':'ok','refreshed':changed}
def refresh_youtube()->Dict[str,Any]:
    cid=get_secret('GOOGLE_CLIENT_ID',''); cs=get_secret('GOOGLE_CLIENT_SECRET','')
    if not cid or not cs: return {'status':'skipped','missing':['GOOGLE_CLIENT_ID','GOOGLE_CLIENT_SECRET']}
    changed=0
    with SessionLocal() as s:
        rows=s.query(Token).filter(Token.platform=='youtube').all()
        for r in rows:
            if not r.refresh_token: continue
            try:
                res=requests.post('https://oauth2.googleapis.com/token',data={
                    'client_id':cid,'client_secret':cs,'grant_type':'refresh_token','refresh_token':r.refresh_token
                },timeout=20).json()
                if res.get('access_token'):
                    r.access_token=res['access_token']
                    ei=res.get('expires_in')
                    if ei: r.expires_at=_now()+datetime.timedelta(seconds=int(ei))
                    changed+=1
            except Exception: pass
        s.commit()
    return {'status':'ok','refreshed':changed}
def refresh_all()->Dict[str,Any]:
    return {'facebook_instagram':refresh_facebook_and_instagram(),'tiktok':refresh_tiktok(),'youtube':refresh_youtube()}
