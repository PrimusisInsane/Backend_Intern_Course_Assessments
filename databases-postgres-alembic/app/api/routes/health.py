from fastapi import APIRouter
from app.core.database import engine
from app.core.mongo import client

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/postgres")
def postgres_health():
    try:
        conn = engine.connect()
        conn.close()
        return {"postgres": "ok"}
    except Exception as e:
        return {"postgres": "fail", "error": str(e)}


@router.get("/mongo")
async def mongo_health():
    try:
        await client.admin.command("ping")
        return {"mongo": "ok"}
    except Exception as e:
        return {"mongo": "fail", "error": str(e)}