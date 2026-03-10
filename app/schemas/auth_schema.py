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
    password: str = Field(..., min_length=6, max_length=100) # bắt buộc (...)
    fullName: str = Field(..., min_length=1, max_length=100)
    phoneNumber: Optional[str] = None # bỏ qua giá trị mặc định là None
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


class ResendOtpRequest(BaseModel):
    """Resend OTP request schema (without authentication)"""
    email: EmailStr


class SendOtpRequest(BaseModel):
    """Send OTP to authenticated user's email - no body needed, uses token"""
    pass


class VerifyOtpWithTokenRequest(BaseModel):
    """Verify OTP with access token"""
    otp: str = Field(..., min_length=4, max_length=10)


# ========================================================
# Response Schemas - Auth
# ========================================================

class AuthResponse(ResponseBase):
    """Auth response with tokens"""
    data: Optional[TokenResponse] = None


# ========================================================
# Profile Schemas
# ========================================================

class ProfileResponse(BaseModel):
    """Profile response schema"""
    id: int
    email: str
    fullName: Optional[str] = None
    phoneNumber: Optional[str] = None
    avatarUrl: Optional[str] = None
    address: Optional[str] = None
    role: str
    emailVerified: bool
    subscriptionType: str
    subscriptionStart: Optional[str] = None
    subscriptionEnd: Optional[str] = None
    isActive: bool

    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):
    """Update profile request schema"""
    fullName: Optional[str] = Field(None, min_length=1, max_length=100)
    phoneNumber: Optional[str] = Field(None, max_length=20)
    avatarUrl: Optional[str] = Field(None, max_length=500)
    address: Optional[str] = Field(None, max_length=255)


# ========================================================
# Subscription Schemas
# ========================================================

class SubscriptionRequest(BaseModel):
    """Subscription request schema"""
    subscription_type: str = Field(..., pattern="^(plus|pro|vip|max)$")


class SubscriptionResponse(BaseModel):
    """Subscription response schema"""
    subscriptionType: str
    subscriptionStart: str
    subscriptionEnd: str
    isActive: bool