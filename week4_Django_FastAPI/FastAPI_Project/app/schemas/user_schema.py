from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    password: str

class UserResponse(BaseModel):  
    id: int
    name: str
    email: str
    age: int
    tasks: List["TaskResponse"] = [] 
    role : str

    class Config:
        from_attributes = True

from app.schemas.task_schema import TaskResponse 
UserResponse.model_rebuild()