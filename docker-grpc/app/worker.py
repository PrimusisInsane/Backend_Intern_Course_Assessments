from arq.connections import RedisSettings
from app.core.config import settings
from app.db.database import SessionLocal
from app.db.mongo import activity_feed_collection
from app.repositories.activity_log_repo import create_log
from datetime import datetime, timezone
import logging

logging.getLogger("arq").setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

async def write_activity_log(ctx, user_id: int, action: str, task_id: int = None, project_id: int = None, detail: str = None):
    db = SessionLocal()
    try:
        log = create_log(db, user_id, action, task_id=task_id, project_id=project_id, detail=detail)

        await activity_feed_collection.insert_one({
            "log_id": log.id,
            "user_id": user_id,
            "task_id": task_id,
            "project_id": project_id,
            "action": action,
            "detail": detail,
            "created_at": datetime.now(timezone.utc).isoformat()
        })

        print(f"[ARQ] Logged: {action} for user {user_id} (Postgres + Mongo)")
    except Exception as e:
        print(f"[ARQ] FAILED to log: {e}")
        raise
    finally:
        db.close()


class WorkerSettings:
    functions = [write_activity_log]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)