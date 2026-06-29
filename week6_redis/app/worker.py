from arq.connections import RedisSettings
from app.core.config import settings
from app.db.database import SessionLocal
from app.repositories.activity_log_repo import create_log
import logging

logging.getLogger("arq").setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


async def write_activity_log(ctx, user_id: int, action: str, task_id: int = None, project_id: int = None, detail: str = None):
    db = SessionLocal()
    try:
        create_log(db, user_id, action, task_id=task_id, project_id=project_id, detail=detail)
        print(f"[ARQ] Logged: {action} for user {user_id}")
    except Exception as e:
        print(f"[ARQ] FAILED to log: {e}")
        raise
    finally:
        db.close()


class WorkerSettings:
    functions = [write_activity_log]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)