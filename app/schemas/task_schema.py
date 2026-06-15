from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    project_id: int
    user_id: int

class TaskResponse(BaseModel):  
    id: int
    title: str
    user_id: int
    project_id: int

    class Config:
        from_attributes = True