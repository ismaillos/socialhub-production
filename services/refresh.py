import datetime, requests
from typing import Dict, Any
from db.database import SessionLocal
from db.models import Token
from core.providers import get_provider_secrets

def _now(): return datetime.datetime.utcnow()

def refresh_facebook_and_instagram() -> Dict[str, Any]:
    cfg, missing = get_provider_secrets(["FACEBOOK_CLIENT_ID", "FACEBOOK_CLIENT_SECRET"])
    if missing:
        return {"status":"skipped","missing":missing}
    client_id = cfg["FACEBOOK_CLIENT_ID"]; client_secret = cfg["FACEBOOK_CLIENT_SECRET"]
    changed = 0; pages_updated = 0
    with SessionLocal() as s:
        rows = s.query(Token).filter(Token.platform.in_(["facebook","instagram"])).all()
        for r in rows:
            if r.access_token:
                try:
                    res = requests.get("https://graph.facebook.com/v19.0/oauth/access_token", params={
                        "grant_type":"fb_exchange_token",
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "fb_exchange_token": r.access_token
                    }, timeout=20).json()
                    new_user_token = res.get("access_token")
                    expires_in = res.get("expires_in")
                    if new_user_token:
                        r.access_token = new_user_token
                        if expires_in:
                            r.expires_at = _now() + datetime.timedelta(seconds=int(expires_in))
                        changed += 1
                except Exception:
                    pass
            if r.page_id and r.access_token:
                try:
                    pg = requests.get(f"https://graph.facebook.com/{r.page_id}", params={
                        "fields":"name,access_token",
                        "access_token": r.access_token
                    }, timeout=20).json()
                    page_token = pg.get("access_token")
                    if page_token:
                        r.page_access_token = page_token
                        pages_updated += 1
                except Exception:
                    pass
        s.commit()
    return {"status":"ok","user_tokens_refreshed": changed, "page_tokens_updated": pages_updated}

def refresh_tiktok() -> Dict[str, Any]:
    cfg, missing = get_provider_secrets(["TIKTOK_CLIENT_KEY","TIKTOK_CLIENT_SECRET"])
    if missing:
        return {"status":"skipped","missing":missing}
    changed = 0
    with SessionLocal() as s:
        rows = s.query(Token).filter(Token.platform=="tiktok").all()
        for r in rows:
            if not r.refresh_token: continue
            try:
                res = requests.post("https://open-api.tiktok.com/oauth/refresh_token/", data={
                    "client_key": cfg["TIKTOK_CLIENT_KEY"],
                    "grant_type": "refresh_token",
                    "refresh_token": r.refresh_token
                }, timeout=20).json()
                if res.get("data") and res["data"].get("access_token"):
                    r.access_token = res["data"]["access_token"]
                    r.refresh_token = res["data"].get("refresh_token", r.refresh_token)
                    expires_in = res["data"].get("expires_in")
                    if expires_in:
                        r.expires_at = _now() + datetime.timedelta(seconds=int(expires_in))
                    changed += 1
            except Exception:
                pass
        s.commit()
    return {"status":"ok","refreshed": changed}

def refresh_youtube() -> Dict[str, Any]:
    cfg, missing = get_provider_secrets(["GOOGLE_CLIENT_ID","GOOGLE_CLIENT_SECRET"])
    if missing:
        return {"status":"skipped","missing":missing}
    changed = 0
    with SessionLocal() as s:
        rows = s.query(Token).filter(Token.platform=="youtube").all()
        for r in rows:
            if not r.refresh_token: continue
            try:
                res = requests.post("https://oauth2.googleapis.com/token", data={
                    "client_id": cfg["GOOGLE_CLIENT_ID"],
                    "client_secret": cfg["GOOGLE_CLIENT_SECRET"],
                    "grant_type": "refresh_token",
                    "refresh_token": r.refresh_token
                }, timeout=20).json()
                if res.get("access_token"):
                    r.access_token = res["access_token"]
                    expires_in = res.get("expires_in")
                    if expires_in:
                        r.expires_at = _now() + datetime.timedelta(seconds=int(expires_in))
                    changed += 1
            except Exception:
                pass
        s.commit()
    return {"status":"ok","refreshed": changed}

def refresh_all() -> Dict[str, Any]:
    return {
        "facebook_instagram": refresh_facebook_and_instagram(),
        "tiktok": refresh_tiktok(),
        "youtube": refresh_youtube(),
    }
