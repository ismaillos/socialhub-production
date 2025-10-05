from fastapi import APIRouter
from db.database import SessionLocal
from db.models import Token

router = APIRouter(prefix="/auth", tags=["Status"])

@router.get("/status")
def get_status():
    session = SessionLocal()
    tokens = session.query(Token).all()
    session.close()
    return {
        t.platform: True for t in tokens
    }
