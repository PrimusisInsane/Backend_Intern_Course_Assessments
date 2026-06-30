from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.project_model import Project
    from app.models.user_model import User


class Membership(Base):
    __tablename__ = "memberships"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), primary_key=True)

    user: Mapped["User"] = relationship("User", back_populates="memberships")
    project: Mapped["Project"] = relationship("Project", back_populates="memberships")
