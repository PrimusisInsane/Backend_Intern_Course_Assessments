from fastapi import FastAPI

from app.api.routes import user, project, task, health

app = FastAPI(title="Backend Project")

app.include_router(user.router)
app.include_router(project.router)
app.include_router(task.router)
app.include_router(health.router)


@app.get("/")
def root():
    return {"message": "API running"}