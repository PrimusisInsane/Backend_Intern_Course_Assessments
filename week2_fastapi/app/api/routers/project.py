from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

project_db = []
project_id_counter = 1


class ProjectCreate(BaseModel):
    Project_Name: str
    Project_Details: str | None = None
    status: bool = False


@router.post("/projects")              # CREATE TASK
def create_project(project: ProjectCreate):
    global project_id_counter

    project_data = project.model_dump()
    project_data["id"] = project_id_counter
    project_id_counter += 1

    project_db.append(project_data)

    return {
        "message": "Project created",
        "project": project_data
    }



@router.get("/projects")       # GET ALL TASKS
def get_project():
    return project_db



@router.get("/projects/{project_id}")     # GET TASK BY ID
def get_project(project_id: int):
    for project in project_db:
        if project["id"] == project_id:
            return project

    return {"message": "Project not found"}



@router.put("/projects/{project_id}")         # UPDATE TASK (PUT)
def update_project(project_id: int, updated_project: ProjectCreate):
    for project in project_db:
        if project["id"] == project_id:
            project["Project_Name"] = updated_project.Project_Name
            project["Project_Details"] = updated_project.Project_Details
            project["status"] = updated_project.status

            return {
                "message": "Project updated",
                "project": project
            }

    return {"message": "Project not found"}


@router.delete("/projects/{project_id}")              # DELETE TASK
def delete_project(project_id: int):
    for index, project in enumerate(project_db):
        if project["id"] == project_id:
            removed = project_db.pop(index)
            return {
                "message": "Project deleted",
                "Project": removed
            }

    return {"message": "Project not found"}