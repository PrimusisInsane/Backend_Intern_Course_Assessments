from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGODB_URL)
mongo_db = mongo_client[settings.DB_NAME]
activity_feed_collection = mongo_db["activity_feed"]
