from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    memberships = relationship("Membership", back_populates="project")
    users = relationship("User", secondary="memberships", back_populates="projects")

    tasks = relationship("Task", back_populates="project")