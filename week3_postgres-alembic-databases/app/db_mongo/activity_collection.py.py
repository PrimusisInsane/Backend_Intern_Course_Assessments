from app.core.mongo import db

activity_collection = db["activities"]

async def log_activity(data: dict):
    return await activity_collection.insert_one(data)

async def get_activities():
    cursor = activity_collection.find()
    return await cursor.to_list(length=100)