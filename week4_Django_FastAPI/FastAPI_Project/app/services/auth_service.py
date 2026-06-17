from sqlalchemy.orm import Session
from app.repositories.user_repo import get_user_by_email, create_user
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user_schema import UserCreate
from fastapi import HTTPException

def register_service(db: Session, data: UserCreate):
    existing_user = get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(data.password)
    return create_user(db, data.name, data.email, data.age, hashed)

def login_service(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}