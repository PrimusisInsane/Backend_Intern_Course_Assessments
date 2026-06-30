from fastapi import APIRouter

from app.db.database import engine

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/db")
def db_health():
    try:
        conn = engine.connect()
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "fail", "detail": str(e)}
