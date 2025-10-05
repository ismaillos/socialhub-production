from db.database import SessionLocal
from db.models import Token

account_id = channel_json["items"][0]["id"] if "items" in channel_json else "unknown"

session = SessionLocal()
existing = session.query(Token).filter(Token.platform == "youtube").first()
if existing:
    existing.access_token = access_token
    existing.refresh_token = refresh_token
    existing.account_id = account_id
    session.commit()
else:
    new_token = Token(
        platform="youtube",
        account_id=account_id,
        access_token=access_token,
        refresh_token=refresh_token
    )
    session.add(new_token)
    session.commit()
session.close()
