from app.repositories.user_repo import create_user, get_users, get_user_by_id, delete_user, update_user
from app.models.task_model import Task

def create_user_service(db, name: str, email: str, age: int, password: str):
    return create_user(db, name, email, age, password)

def list_users_service(db):
    return get_users(db)

def get_user_service(db, user_id):
    return get_user_by_id(db, user_id)

def get_user_by_id_service(db, user_id):
    return get_user_by_id(db, user_id)

def delete_user_service(db, user_id):
    return delete_user(db, user_id)

def update_user_service(db, user_id, name: str, email: str, age: int):
    return update_user(db, user_id, name, email, age)

def get_user_tasks_service(db, user_id):
    return db.query(Task).filter(Task.user_id == user_id).all()