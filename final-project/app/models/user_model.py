from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.membership_model import Membership
    from app.models.project_model import Project
    from app.models.task_model import Task


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, default="member")

    memberships: Mapped[List["Membership"]] = relationship("Membership", back_populates="user")
    projects: Mapped[List["Project"]] = relationship(
        "Project", secondary="memberships", back_populates="users"
    )
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="user")
