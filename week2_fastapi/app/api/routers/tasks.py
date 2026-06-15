from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

tasks_db = []
task_id_counter = 1


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False


@router.post("/tasks")              # CREATE TASK
def create_task(task: TaskCreate):
    global task_id_counter

    task_data = task.model_dump()
    task_data["id"] = task_id_counter
    task_id_counter += 1

    tasks_db.append(task_data)

    return {
        "message": "Task created",
        "task": task_data
    }



@router.get("/tasks")       # GET ALL TASKS
def get_tasks():
    return tasks_db



@router.get("/tasks/{task_id}")     # GET TASK BY ID
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task

    return {"message": "Task not found"}



@router.put("/tasks/{task_id}")         # UPDATE TASK (PUT)
def update_task(task_id: int, updated_task: TaskCreate):
    for task in tasks_db:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["description"] = updated_task.description
            task["completed"] = updated_task.completed

            return {
                "message": "Task updated",
                "task": task
            }

    return {"message": "Task not found"}


@router.delete("/tasks/{task_id}")              # DELETE TASK
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            removed = tasks_db.pop(index)
            return {
                "message": "Task deleted",
                "task": removed
            }

    return {"message": "Task not found"}