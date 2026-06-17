from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer)
    password = Column(String, nullable=False)   
    role = Column(String, default="member")
    

    memberships = relationship("Membership", back_populates="user")
    projects = relationship("Project", secondary="memberships", back_populates="users")
    tasks = relationship("Task", back_populates="user")