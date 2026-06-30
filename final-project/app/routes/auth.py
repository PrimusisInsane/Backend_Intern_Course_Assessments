from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.auth_service import login_service, register_service


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    age: int
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = register_service(db, payload.name, payload.email, payload.age, payload.password)
    return {"id": user.id, "email": user.email}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return login_service(db, payload.email, payload.password)
