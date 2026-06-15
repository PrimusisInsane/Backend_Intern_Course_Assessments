from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship


class Membership(Base):
    __tablename__ = "memberships"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)

    user = relationship("User", back_populates="memberships")
    project = relationship("Project", back_populates="memberships")