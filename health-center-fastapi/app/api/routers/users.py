from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import time

router = APIRouter()

users_db = []
id_counter = 1


class UserCreate(BaseModel):
    name: str
    email: str
    age: int | None = None



def log_user_creation(user: dict):      # Background task
    time.sleep(2)
    print(f"[AUDIT LOG] User created: {user}")


@router.post("/users")      # CREATE USER
def create_user(user: UserCreate, background_tasks: BackgroundTasks):
    global id_counter

    user_data = user.model_dump()
    user_data["id"] = id_counter
    id_counter += 1

    users_db.append(user_data)

    background_tasks.add_task(log_user_creation, user_data)

    return {
        "message": "User created",
        "user": user_data
    }


@router.get("/users")       # GET ALL USERS
def get_users():
    return users_db



@router.get("/users/{user_id}")     # GET USER BY ID
def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user

    return {"message": "User not found"}



@router.put("/users/{user_id}")         # UPDATE USER (PUT)
def update_user(user_id: int, updated_user: UserCreate):
    for user in users_db:
        if user["id"] == user_id:
            user["name"] = updated_user.name
            user["email"] = updated_user.email
            user["age"] = updated_user.age

            return {
                "message": "User updated",
                "user": user
            }

    return {"message": "User not found"}


@router.delete("/users/{user_id}")      # DELETE USER
def delete_user(user_id: int):
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            removed = users_db.pop(index)
            return {
                "message": "User deleted",
                "user": removed
            }

    return {"message": "User not found"}