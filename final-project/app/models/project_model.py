from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.membership_model import Membership
    from app.models.task_model import Task
    from app.models.user_model import User


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    memberships: Mapped[List["Membership"]] = relationship(
        "Membership", back_populates="project", cascade="all, delete-orphan"
    )
    users: Mapped[List["User"]] = relationship(
        "User", secondary="memberships", back_populates="projects"
    )
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="project")
