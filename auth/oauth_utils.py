import requests
from fastapi.responses import RedirectResponse
from db.database import SessionLocal
from db.models import Token

def save_token(platform, account_id, username, profile_pic, access_token):
    session = SessionLocal()
    existing = session.query(Token).filter(Token.platform == platform).first()
    if existing:
        existing.access_token = access_token
        existing.account_id = account_id
        existing.username = username
        existing.profile_pic = profile_pic
    else:
        new_token = Token(
            platform=platform,
            account_id=account_id,
            username=username,
            profile_pic=profile_pic,
            access_token=access_token,
        )
        session.add(new_token)
    session.commit()
    session.close()

def success_redirect():
    return RedirectResponse(url="/accounts")
