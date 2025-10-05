from db.database import SessionLocal
from db.models import Token

account_id = user_json.get("username", "unknown")

session = SessionLocal()
existing = session.query(Token).filter(Token.platform == "pinterest").first()
if existing:
    existing.access_token = access_token
    existing.account_id = account_id
    session.commit()
else:
    new_token = Token(platform="pinterest", account_id=account_id, access_token=access_token)
    session.add(new_token)
    session.commit()
session.close()
