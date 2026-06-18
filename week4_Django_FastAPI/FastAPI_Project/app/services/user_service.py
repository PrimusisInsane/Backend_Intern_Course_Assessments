from app.repositories.user_repo import create_user, get_users, get_user_by_id, delete_user, update_user
from app.models.task_model import Task

def create_user_service(db, data):
    return create_user(db, data.name, data.email, data.age, data.password) 

def list_users_service(db):
    return get_users(db)

def get_user_service(db, user_id):
    return get_user_by_id(db, user_id)

def get_user_by_id_service(db, user_id): 
    return get_user_by_id(db, user_id)

def delete_user_service(db, user_id):
    return delete_user(db, user_id)

def update_user_service(db, user_id, data):
    return update_user(db, user_id, data.name, data.email, data.age)

def get_user_tasks_service(db, user_id):
    return db.query(Task).filter(Task.user_id == user_id).all()