from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import health, users, tasks, project
from app.middleware.middleware_1 import TimingMiddleware
from app.exceptions.exception_handlers import (
    http_exception_handler,
    validation_exception_handler
)

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    key=settings.API_KEY
)

app.include_router(health.router, tags=["Health"])
app.include_router(users.router, tags=["Users"])
app.include_router(tasks.router, tags=["Tasks"])
app.include_router(project.router, tags = ["Project"])

app.add_middleware(TimingMiddleware)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/")
def root():
    return {"message": "API is running"}