import os
from sqlalchemy.exc import OperationalError
from db.database import SessionLocal
from db.models import AppSecret
from util.secret_box import decrypt_value
def get_secret(name: str, default: str | None = None) -> str | None:
    val = os.getenv(name)
    if val: return val
    try:
        with SessionLocal() as s:
            row = s.query(AppSecret).filter(AppSecret.key == name).first()
            if row and row.value_enc:
                try: return decrypt_value(row.value_enc)
                except Exception: return default
    except OperationalError:
        return default
    return default
