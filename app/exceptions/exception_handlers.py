from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,                # HTTP exceptions (404, etc.)
        content={
            "success": False,
            "message": exc.detail
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,            # Validation errors (Pydantic)
        content={
            "success": False,
            "message": "Validation Error",
            "detail": exc.errors()
        }
    )