from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.security import create_access_token, hash_password, verify_password
from app.repositories.user_repo import create_user, get_user_by_email


def register_service(db: Session, name: str, email: str, age: int, password: str):
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(password)
    return create_user(db, name, email, age, hashed)


def login_service(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
