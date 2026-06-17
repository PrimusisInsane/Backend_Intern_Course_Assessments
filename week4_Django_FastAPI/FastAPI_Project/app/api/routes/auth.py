from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_schema import UserCreate
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.services.auth_service import register_service, login_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_service(db, user)

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    return login_service(db, credentials.email, credentials.password)