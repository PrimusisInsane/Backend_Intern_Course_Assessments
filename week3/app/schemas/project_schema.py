from pydantic import BaseModel
from typing import List

class ProjectCreate(BaseModel):
    name: str

class ProjectResponse(BaseModel):
    id: int
    name: str
    tasks: List["TaskResponse"] = []  
    class Config:
        from_attributes = True

from app.schemas.task_schema import TaskResponse  
ProjectResponse.model_rebuild()