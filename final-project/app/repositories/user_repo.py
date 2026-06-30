from sqlalchemy.orm import Session

from app.models.user_model import User


def create_user(db: Session, name: str, email: str, age: int, password: str, role: str = "member"):
    user = User(name=name, email=email, age=age, password=password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update_user(
    db: Session,
    user_id: int,
    name: str = None,
    email: str = None,
    age: int = None,
    password: str = None,
    role: str = None,
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    if name is not None:
        user.name = name
    if email is not None:
        user.email = email
    if age is not None:
        user.age = age
    if password is not None:
        user.password = password
    if role is not None:
        user.role = role
    db.commit()
    db.refresh(user)
    return user
