from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("sentrix")


class AppException(Exception):
    """Base exception for application errors."""
    def __init__(self, status_code: int, detail: str, error_code: str = "INTERNAL_ERROR"):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code


class NotFoundException(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail, error_code="NOT_FOUND")


class AuthorizationException(AppException):
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(status_code=403, detail=detail, error_code="FORBIDDEN")


class ValidationException(AppException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=422, detail=detail, error_code="VALIDATION_ERROR")


async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"AppException at {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error_code, "detail": exc.detail},
    )


async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception at {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"error": "INTERNAL_ERROR", "detail": "An unexpected error occurred."},
    )
