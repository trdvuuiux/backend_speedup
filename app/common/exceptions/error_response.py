from typing import Optional, Any, Dict
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response"""
    errorCode: str
    errorMessage: str
    errorDetails: Optional[Any] = None


def get_error_response(
    error_code: str,
    error_message: str,
    error_details: Optional[Any] = None
) -> Dict:
    """Get error response dict"""
    return {
        "success": False,
        "errorCode": error_code,
        "errorMessage": error_message,
        "errorDetails": error_details,
        "data": None
    }


# Error codes
class ErrorCode:
    # Common errors
    BAD_REQUEST = "BAD_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    
    # Auth errors (2xx)
    AUTH_202 = "202"       # Invalid data type or JSON
    AUTH_221 = "221"       # Default role not found
    AUTH_227 = "227"       # User not found
    AUTH_233 = "233"       # Email not verified
    AUTH_234 = "234"       # Refresh token expired
    AUTH_238 = "238"       # Email does not exist
    AUTH_239 = "239"       # Password incorrect
    AUTH_243 = "243"       # Required fields missing
    AUTH_248 = "248"       # Refresh token revoked
    AUTH_249 = "249"       # User blocked
    AUTH_255 = "255"       # Email already exists
