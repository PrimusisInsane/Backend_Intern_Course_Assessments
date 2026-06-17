from fastapi import APIRouter
from app.core.database import engine

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/postgres")
def postgres_health():
    try:
        conn = engine.connect()
        conn.close()
        return {"postgres": "ok"}
    except Exception as e:
        return {"postgres": "fail", "error": str(e)}


