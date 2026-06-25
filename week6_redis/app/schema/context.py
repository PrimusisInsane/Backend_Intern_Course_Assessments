from app.db.database import SessionLocal
from app.db.security import decode_access_token
from app.repositories.user_repo import get_user_by_id
from app.db.redis import get_arq_pool, redis_client

async def get_context(request, data=None):
    db = SessionLocal()
    request.state.db_session = db
    user = None

    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = decode_access_token(token)
            user_id = int(payload.get("sub"))
            user = get_user_by_id(db, user_id)
        except Exception:
            user = None

    try:
        redis_pool = await get_arq_pool()
    except Exception:
        redis_pool = None

    return {"db": db, "user": user, "request": request, "redis": redis_pool, "cache": redis_client}