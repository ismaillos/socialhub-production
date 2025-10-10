import datetime
from db.database import SessionLocal
from db.models import Token
from services.refresh import refresh_youtube, refresh_tiktok, refresh_facebook_and_instagram
MARGIN = datetime.timedelta(minutes=10)
def ensure_fresh(platform:str, account_id:str|None=None)->Token|None:
    with SessionLocal() as s:
        q=s.query(Token).filter(Token.platform==platform)
        if account_id: q=q.filter(Token.account_id==account_id)
        t=q.first()
        if not t: return None
        if t.expires_at and (t.expires_at - datetime.datetime.utcnow()) < MARGIN:
            if platform=='youtube': refresh_youtube()
            elif platform=='tiktok': refresh_tiktok()
            elif platform in ('facebook','instagram'): refresh_facebook_and_instagram()
            s.refresh(t)
        return t
