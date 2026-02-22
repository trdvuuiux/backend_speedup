from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth_schema import (
    SignUpRequest,
    LoginRequest,
    RefreshTokenRequest,
    LogoutRequest,
    VerifyOtpRequest,
    AuthResponse,
    TokenResponse,
)
from app.crud.auth_crud import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    verify_user_password,
    update_user_tokens,
    clear_user_tokens,
    verify_otp,
    generate_tokens_for_user,
)
from app.services.email_service import send_otp_email
from app.core.security import decode_token
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Auth"])


# ========================================================
# POST /api/auth/signup
# ========================================================
@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    """
    Register a new user and send OTP to email for verification.
    Returns access and refresh tokens after successful registration.
    """
    # Check if email already exists
    existing_user = get_user_by_email(db, request.email)
    if existing_user:
        return AuthResponse(
            success=False,
            errorCode="255",
            errorMessage="Email already exists",
            data=None
        )
    
    # Create new user
    try:
        user = create_user(
            db=db,
            email=request.email,
            password=request.password,
            full_name=request.fullName
        )
    except Exception as e:
        return AuthResponse(
            success=False,
            errorCode="BAD_REQUEST",
            errorMessage=f"Failed to create user: {str(e)}",
            data=None
        )
    
    # Send OTP email (async)
    try:
        await send_otp_email(
            to_email=user.email,
            otp=user.otp,
            full_name=user.full_name or user.username
        )
    except Exception as e:
        # Log error but don't fail the registration
        print(f"Failed to send OTP email: {str(e)}")
    
    # Generate tokens
    tokens = generate_tokens_for_user(user)
    
    # Update user tokens in database
    update_user_tokens(
        db=db,
        user_id=user.id,
        access_token=tokens["accessToken"],
        refresh_token=tokens["refreshToken"]
    )
    
    return AuthResponse(
        success=True,
        data=TokenResponse(**tokens)
    )


# ========================================================
# POST /api/auth/login
# ========================================================
@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate with email and password and return access and refresh tokens.
    """
    # Validate required fields
    if not request.email or not request.password:
        return AuthResponse(
            success=False,
            errorCode="243",
            errorMessage="Email and password are required",
            data=None
        )
    
    # Verify credentials
    user = verify_user_password(db, request.email, request.password)
    
    if not user:
        # Check if email exists to provide specific error
        existing_user = get_user_by_email(db, request.email)
        if not existing_user:
            return AuthResponse(
                success=False,
                errorCode="238",
                errorMessage="Email does not exist",
                data=None
            )
        else:
            return AuthResponse(
                success=False,
                errorCode="239",
                errorMessage="Password is incorrect",
                data=None
            )
    
    # Generate tokens
    tokens = generate_tokens_for_user(user)
    
    # Update user tokens in database
    update_user_tokens(
        db=db,
        user_id=user.id,
        access_token=tokens["accessToken"],
        refresh_token=tokens["refreshToken"]
    )
    
    return AuthResponse(
        success=True,
        data=TokenResponse(**tokens)
    )


# ========================================================
# POST /api/auth/refresh
# ========================================================
@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Rotate refresh token and return a new token pair.
    """
    # Validate required fields
    if not request.refreshToken:
        return AuthResponse(
            success=False,
            errorCode="243",
            errorMessage="Refresh token is required",
            data=None
        )
    
    # Decode refresh token
    payload = decode_token(request.refreshToken)
    
    if not payload:
        return AuthResponse(
            success=False,
            errorCode="UNAUTHORIZED",
            errorMessage="Invalid refresh token",
            data=None
        )
    
    # Check token type
    if payload.get("type") != "refresh":
        return AuthResponse(
            success=False,
            errorCode="UNAUTHORIZED",
            errorMessage="Invalid token type",
            data=None
        )
    
    # Get user from token
    try:
        user_id = int(payload.get("sub"))
    except (ValueError, TypeError):
        return AuthResponse(
            success=False,
            errorCode="UNAUTHORIZED",
            errorMessage="Invalid token payload",
            data=None
        )
    
    # Get user from database
    user = get_user_by_id(db, user_id)
    
    if not user:
        return AuthResponse(
            success=False,
            errorCode="227",
            errorMessage="User not found",
            data=None
        )
    
    # Verify refresh token matches
    if user.refresh_token != request.refreshToken:
        return AuthResponse(
            success=False,
            errorCode="248",
            errorMessage="Refresh token is revoked or does not match",
            data=None
        )
    
    # Generate new tokens
    tokens = generate_tokens_for_user(user)
    
    # Update user tokens in database (rotate)
    update_user_tokens(
        db=db,
        user_id=user.id,
        access_token=tokens["accessToken"],
        refresh_token=tokens["refreshToken"]
    )
    
    return AuthResponse(
        success=True,
        data=TokenResponse(**tokens)
    )


# ========================================================
# POST /api/auth/logout
# ========================================================
@router.post("/logout", response_model=AuthResponse)
async def logout(request: LogoutRequest, db: Session = Depends(get_db)):
    """
    Revoke a refresh token.
    """
    # Validate required fields
    if not request.refreshToken:
        return AuthResponse(
            success=False,
            errorCode="243",
            errorMessage="Refresh token is required",
            data=None
        )
    
    # Decode token to get user
    payload = decode_token(request.refreshToken)
    
    if payload:
        try:
            user_id = int(payload.get("sub"))
            # Clear user tokens
            clear_user_tokens(db, user_id)
        except (ValueError, TypeError):
            pass
    
    # Logout is idempotent for unknown tokens
    return AuthResponse(
        success=True,
        data=None
    )


# ========================================================
# POST /api/auth/verify-otp
# ========================================================
@router.post("/verify-otp", response_model=AuthResponse)
async def verify_otp(request: VerifyOtpRequest, db: Session = Depends(get_db)):
    """
    Verify OTP and activate user account.
    """
    # Validate required fields
    if not request.email or not request.otp:
        return AuthResponse(
            success=False,
            errorCode="243",
            errorMessage="Email and OTP are required",
            data=None
        )
    
    # Verify OTP
    user = verify_otp(db, request.email, request.otp)
    
    if not user:
        # Check if user exists
        existing_user = get_user_by_email(db, request.email)
        if not existing_user:
            return AuthResponse(
                success=False,
                errorCode="238",
                errorMessage="Email does not exist",
                data=None
            )
        else:
            return AuthResponse(
                success=False,
                errorCode="UNAUTHORIZED",
                errorMessage="Invalid or expired OTP",
                data=None
            )
    
    # Generate tokens for verified user
    tokens = generate_tokens_for_user(user)
    
    # Update user tokens in database
    update_user_tokens(
        db=db,
        user_id=user.id,
        access_token=tokens["accessToken"],
        refresh_token=tokens["refreshToken"]
    )
    
    return AuthResponse(
        success=True,
        data=TokenResponse(**tokens)
    )
