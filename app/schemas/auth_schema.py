from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ========================================================
# Response Schemas
# ========================================================

class ResponseBase(BaseModel):
    """Base response model"""
    success: bool = True
    errorCode: Optional[str] = None
    errorMessage: Optional[str] = None


class TokenData(ResponseBase):
    """Token response data"""
    data: Optional[dict] = None


class TokenResponse(BaseModel):
    """Token response schema"""
    accessToken: str
    refreshToken: str
    accessExpireIn: int
    refreshExpireIn: int


# ========================================================
# Request Schemas - Auth
# ========================================================

class SignUpRequest(BaseModel):
    """Sign up request schema"""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    fullName: str = Field(..., min_length=1, max_length=100)
    phoneNumber: Optional[str] = None
    avatarUrl: Optional[str] = None
    address: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refreshToken: str


class LogoutRequest(BaseModel):
    """Logout request schema"""
    refreshToken: str


class VerifyOtpRequest(BaseModel):
    """Verify OTP request schema"""
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=10)


# ========================================================
# Response Schemas - Auth
# ========================================================

class AuthResponse(ResponseBase):
    """Auth response with tokens"""
    data: Optional[TokenResponse] = None
