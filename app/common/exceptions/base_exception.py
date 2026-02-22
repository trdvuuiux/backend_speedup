from typing import Optional, Any, Dict
from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base exception for application"""
    
    def __init__(
        self,
        status_code: int,
        error_code: str,
        error_message: str,
        error_details: Optional[Any] = None
    ):
        super().__init__(status_code=status_code, detail={
            "errorCode": error_code,
            "errorMessage": error_message,
            "errorDetails": error_details
        })
        self.error_code = error_code
        self.error_message = error_message
        self.error_details = error_details


class BadRequestException(AppException):
    """400 Bad Request"""
    
    def __init__(
        self,
        error_code: str = "BAD_REQUEST",
        error_message: str = "Bad request",
        error_details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=error_code,
            error_message=error_message,
            error_details=error_details
        )


class UnauthorizedException(AppException):
    """401 Unauthorized"""
    
    def __init__(
        self,
        error_code: str = "UNAUTHORIZED",
        error_message: str = "Unauthorized",
        error_details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=error_code,
            error_message=error_message,
            error_details=error_details
        )


class ForbiddenException(AppException):
    """403 Forbidden"""
    
    def __init__(
        self,
        error_code: str = "FORBIDDEN",
        error_message: str = "Forbidden",
        error_details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=error_code,
            error_message=error_message,
            error_details=error_details
        )


class NotFoundException(AppException):
    """404 Not Found"""
    
    def __init__(
        self,
        error_code: str = "NOT_FOUND",
        error_message: str = "Not found",
        error_details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=error_code,
            error_message=error_message,
            error_details=error_details
        )


class ConflictException(AppException):
    """409 Conflict"""
    
    def __init__(
        self,
        error_code: str = "CONFLICT",
        error_message: str = "Conflict",
        error_details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code=error_code,
            error_message=error_message,
            error_details=error_details
        )
