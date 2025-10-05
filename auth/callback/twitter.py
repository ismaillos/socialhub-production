# ✅ Save or update token in DB
from db.database import SessionLocal
from db.models import Token

session = SessionLocal()
existing = session.query(Token).filter(Token.platform == "twitter").first()
if existing:
    existing.access_token = access_token
    existing.account_id = user_data["data"]["id"]
    session.commit()
else:
    new_token = Token(
        platform="twitter",
        account_id=user_data["data"]["id"],
        access_token=access_token,
        refresh_token=token_data.get("refresh_token")
    )
    session.add(new_token)
    session.commit()
session.close()

return JSONResponse({
    "status": "ok",
    "platform": "twitter",
    "account_id": user_data["data"]["id"],
    "access_token": access_token,
    "message": "Twitter login successful ✅ and token saved to DB"
})
