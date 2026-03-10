from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Account
from app.schemas.auth_schema import (
    SignUpRequest,
    LoginRequest,
    RefreshTokenRequest,
    LogoutRequest,
    VerifyOtpRequest,
    SendOtpRequest,
    VerifyOtpWithTokenRequest,
    ResendOtpRequest,
    AuthResponse,
    TokenResponse,
    ProfileResponse,
    UpdateProfileRequest,
    SubscriptionRequest,
    SubscriptionResponse,
)
from app.crud.auth_crud import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    verify_user_password,
    update_user_tokens,
    clear_user_tokens,
    verify_otp as crud_verify_otp,
    send_otp_for_user,
    verify_otp_for_user,
    generate_tokens_for_user,
    update_user_profile,
)
from app.services.email_service import send_otp_email
from app.core.security import decode_token
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Auth"])
security = HTTPBearer()


# Dependency to get current user from token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db) # cơ chế Dependency Injection của FastAPI
):
    """Get current authenticated user from access token"""
    token = credentials.credentials
    
    # Decode token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "errorCode": "UNAUTHORIZED", "errorMessage": "Invalid token", "data": None}
        )
    
    # Check token type
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "errorCode": "UNAUTHORIZED", "errorMessage": "Invalid token type", "data": None}
        )
    
    # Get user ID
    try:
        user_id = int(payload.get("sub"))
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "errorCode": "UNAUTHORIZED", "errorMessage": "Invalid token payload", "data": None}
        )
    
    # Get user from database
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "errorCode": "238", "errorMessage": "User not found", "data": None}
        )
    
    return user


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
        # If user is already verified, cannot sign up again
        if existing_user.email_verified:
            return AuthResponse(
                success=False,
                errorCode="255",
                errorMessage="Email already exists",
                data=None
            )
        # If user exists but not verified, generate new OTP and resend
        try:
            from app.crud.auth_crud import send_otp_for_user
            user = send_otp_for_user(db, existing_user.id)
            
            # Send OTP email
            try:
                await send_otp_email(
                    to_email=user.email,
                    otp=user.otp,
                    full_name=user.full_name
                )
            except Exception as e:
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
        except Exception as e:
            return AuthResponse(
                success=False,
                errorCode="BAD_REQUEST",
                errorMessage=f"Failed to resend OTP: {str(e)}",
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
            full_name=user.full_name
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
# POST /api/auth/subscription
# ========================================================
@router.post("/subscription", response_model=AuthResponse)
async def subscribe(
    request: SubscriptionRequest,
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Subscribe to a premium plan.
    - plus: 1 month
    - pro: 3 months
    - vip: 6 months
    - max: 12 months
    """
    from datetime import datetime, timedelta
    
    # Map subscription type to duration in months
    subscription_duration = {
        'plus': 1,
        'pro': 3,
        'vip': 6,
        'max': 12
    }
    
    duration_months = subscription_duration.get(request.subscription_type)
    if not duration_months:
        return AuthResponse(
            success=False,
            errorCode="400",
            errorMessage="Invalid subscription type",
            data=None
        )
    
    # Calculate subscription period
    now = datetime.utcnow()
    subscription_end = now + timedelta(days=duration_months * 30)
    
    # Update user subscription
    current_user.subscription_type = request.subscription_type
    current_user.subscription_start = now
    current_user.subscription_end = subscription_end
    current_user.is_active = True
    
    db.commit()
    db.refresh(current_user)
    
    return AuthResponse(
        success=True,
        data=SubscriptionResponse(
            subscriptionType=current_user.subscription_type,
            subscriptionStart=current_user.subscription_start.isoformat(),
            subscriptionEnd=current_user.subscription_end.isoformat(),
            isActive=current_user.is_active
        )
    )


# ========================================================
# GET /api/auth/profile
# ========================================================
@router.get("/profile", response_model=ProfileResponse)
async def get_profile(
    current_user: Account = Depends(get_current_user)
):
    """
    Get current user's profile.
    """
    return ProfileResponse(
        id=current_user.id,
        email=current_user.email,
        fullName=current_user.full_name,
        phoneNumber=current_user.phone_number,
        avatarUrl=current_user.avatar_url,
        address=current_user.address,
        role=current_user.role,
        emailVerified=current_user.email_verified,
        subscriptionType=current_user.subscription_type,
        subscriptionStart=current_user.subscription_start.isoformat() if current_user.subscription_start else None,
        subscriptionEnd=current_user.subscription_end.isoformat() if current_user.subscription_end else None,
        isActive=current_user.is_active
    )


# ========================================================
# PUT /api/auth/profile
# ========================================================
@router.put("/profile", response_model=AuthResponse)
async def update_profile(
    request: UpdateProfileRequest,
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile.
    """
    # Update user profile
    updated_user = update_user_profile(
        db=db,
        user_id=current_user.id,
        full_name=request.fullName,
        phone_number=request.phoneNumber,
        avatar_url=request.avatarUrl,
        address=request.address
    )
    
    if not updated_user:
        return AuthResponse(
            success=False,
            errorCode="238",
            errorMessage="User not found",
            data=None
        )
    
    return AuthResponse(
        success=True,
        data=None
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
# POST /api/auth/otp/verify
# ========================================================
@router.post("/otp/verify", response_model=AuthResponse)
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
    user = crud_verify_otp(db, request.email, request.otp)
    
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


# ========================================================
# POST /api/auth/otp/resend
# ========================================================
@router.post("/otp/resend", response_model=AuthResponse)
async def resend_otp(request: ResendOtpRequest, db: Session = Depends(get_db)):
    """
    Resend OTP to user email (without authentication).
    User must exist and not be verified yet.
    """
    # Validate required fields
    if not request.email:
        return AuthResponse(
            success=False,
            errorCode="243",
            errorMessage="Email is required",
            data=None
        )
    
    # Check if user exists
    user = get_user_by_email(db, request.email)
    if not user:
        return AuthResponse(
            success=False,
            errorCode="238",
            errorMessage="Email does not exist",
            data=None
        )
    
    # Check if user is already verified
    if user.email_verified:
        return AuthResponse(
            success=False,
            errorCode="255",
            errorMessage="Email already verified",
            data=None
        )
    
    # Generate new OTP
    user = send_otp_for_user(db, user.id)
    
    # Send OTP email
    try:
        await send_otp_email(
            to_email=user.email,
            otp=user.otp,
            full_name=user.full_name or "User"
        )
    except Exception as e:
        print(f"Failed to send OTP email: {str(e)}")
    
    return AuthResponse(
        success=True,
        data=None
    )


# ========================================================
# POST /api/auth/otp/send
# ========================================================
@router.post("/otp/send", response_model=AuthResponse)
async def send_email_otp(
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a verification OTP to the authenticated user email.
    OTP TTL is 10 minutes.
    """
    # Generate new OTP and save to user
    user = send_otp_for_user(db, current_user.id)
    
    if not user:
        return AuthResponse(
            success=False,
            errorCode="238",
            errorMessage="User not found",
            data=None
        )
    
    # Send OTP email
    try:
        await send_otp_email(
            to_email=user.email,
            otp=user.otp,
            full_name=user.full_name or "User"
        )
    except Exception as e:
        print(f"Failed to send OTP email: {str(e)}")
    
    return AuthResponse(
        success=True,
        data=None
    )


# ========================================================
# POST /api/auth/email/otp/verify
# ========================================================
@router.post("/email/otp/verify", response_model=AuthResponse)
async def verify_email_otp(
    request: VerifyOtpWithTokenRequest,
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify OTP and issue new access and refresh tokens.
    Max attempts is 5.
    """
    # Validate required fields
    if not request.otp:
        return AuthResponse(
            success=False,
            errorCode="243",
            errorMessage="OTP is required",
            data=None
        )
    
    # Verify OTP for current user
    user = verify_otp_for_user(db, current_user.id, request.otp, max_attempts=5)
    
    if not user:
        # Check user status to determine error
        user = get_user_by_id(db, current_user.id)
        if not user:
            return AuthResponse(
                success=False,
                errorCode="238",
                errorMessage="User not found",
                data=None
            )
        
        # Check if attempts exceeded
        if user.otp_attempts and user.otp_attempts >= 5:
            return AuthResponse(
                success=False,
                errorCode="602",
                errorMessage="OTP attempts exceeded",
                data=None
            )
        
        # Check if OTP is expired
        if user.created_otp:
            from datetime import datetime, timedelta
            expiry_time = user.created_otp + timedelta(minutes=10)
            if datetime.utcnow() > expiry_time:
                return AuthResponse(
                    success=False,
                    errorCode="242",
                    errorMessage="OTP is expired",
                    data=None
                )
        
        return AuthResponse(
            success=False,
            errorCode="602",
            errorMessage="Invalid OTP",
            data=None
        )
    
    # Generate new tokens
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
