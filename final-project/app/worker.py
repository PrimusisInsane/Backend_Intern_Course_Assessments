from datetime import datetime, timezone

from arq.connections import RedisSettings

from app.core.config import settings

if not settings.REDIS_URL:  # noqa: E402
    raise RuntimeError("REDIS_URL is not set. Check your .env file.")  # noqa: E402


REDIS_URL: str = settings.REDIS_URL  # noqa: E402

from app.db.database import SessionLocal  # noqa: E402
from app.db.mongo import activity_feed_collection  # noqa: E402
from app.repositories.activity_log_repo import create_log  # noqa: E402


async def write_activity_log(
    ctx, user_id: int, action: str, task_id: int = None, project_id: int = None, detail: str = None
):
    db = SessionLocal()
    try:
        log = create_log(db, user_id, action, task_id=task_id, project_id=project_id, detail=detail)

        await activity_feed_collection.insert_one(
            {
                "log_id": log.id,
                "user_id": user_id,
                "task_id": task_id,
                "project_id": project_id,
                "action": action,
                "detail": detail,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

        print(f"[ARQ] Logged: {action} for user {user_id} (Postgres + Mongo)")
    except Exception as e:
        print(f"[ARQ] FAILED to log: {e}")
        raise
    finally:
        db.close()


class WorkerSettings:
    functions = [write_activity_log]
    redis_settings = RedisSettings.from_dsn(REDIS_URL)
