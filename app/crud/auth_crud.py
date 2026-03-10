from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.models import Account
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.core.config import settings
import secrets
import string


def generate_otp(length: int = 6) -> str:
    """Generate a random OTP"""
    return ''.join(secrets.choice(string.digits) for _ in range(length))


def create_user(db: Session, email: str, password: str, full_name: str) -> Account:
    """Create a new user"""
    hashed_password = get_password_hash(password)
    
    otp = generate_otp()
    
    db_user = Account(
        email=email,
        password=hashed_password,
        full_name=full_name,
        otp=otp,
        created_otp=datetime.utcnow(),
        role='student'
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Account:
    """Get user by email"""
    return db.query(Account).filter(Account.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Account:
    """Get user by ID"""
    return db.query(Account).filter(Account.id == user_id).first()


def verify_user_password(db: Session, email: str, password: str) -> Account:
    """Verify user credentials"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def update_user_tokens(db: Session, user_id: int, access_token: str, refresh_token: str) -> Account:
    """Update user tokens"""
    user = get_user_by_id(db, user_id)
    if user:
        user.access_token = access_token
        user.refresh_token = refresh_token
        db.commit()
        db.refresh(user)
    return user


def clear_user_tokens(db: Session, user_id: int) -> bool:
    """Clear user tokens (logout)"""
    user = get_user_by_id(db, user_id)
    if user:
        user.access_token = None
        user.refresh_token = None
        user.otp = None
        user.created_otp = None
        db.commit()
        return True
    return False


def verify_otp(db: Session, email: str, otp: str) -> Account:
    """Verify OTP and return user if valid"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    # Check if user is already verified
    if user.email_verified:
        return None
    
    # Check if OTP exists (not None/empty)
    if not user.otp:
        return None
    
    # Check if OTP matches
    if user.otp != otp:
        return None
    
    # Check if OTP is expired (5 minutes)
    if user.created_otp:
        expiry_time = user.created_otp + timedelta(minutes=5)
        if datetime.utcnow() > expiry_time:
            return None
    
    # Clear OTP after successful verification
    user.otp = None
    user.created_otp = None
    user.otp_attempts = 0
    user.email_verified = True
    db.commit()
    db.refresh(user)
    return user


def send_otp_for_user(db: Session, user_id: int) -> Account:
    """Generate and send OTP to user's email (for authenticated user)"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    # Generate new OTP
    otp = generate_otp()
    user.otp = otp
    user.created_otp = datetime.utcnow()
    user.otp_attempts = 0  # Reset attempts
    db.commit()
    db.refresh(user)
    return user


def verify_otp_for_user(db: Session, user_id: int, otp: str, max_attempts: int = 5) -> Account:
    """Verify OTP for authenticated user with attempt tracking"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    # Check if OTP is expired (10 minutes for this endpoint)
    if user.created_otp:
        expiry_time = user.created_otp + timedelta(minutes=10)
        if datetime.utcnow() > expiry_time:
            # Clear OTP and reset attempts
            user.otp = None
            user.created_otp = None
            user.otp_attempts = 0
            db.commit()
            return None
    
    # Check if attempts exceeded
    if user.otp_attempts and user.otp_attempts >= max_attempts:
        return None
    
    # Verify OTP
    if user.otp != otp:
        # Increment attempts
        user.otp_attempts = (user.otp_attempts or 0) + 1
        db.commit()
        return None
    
    # Clear OTP after successful verification
    user.otp = None
    user.created_otp = None
    user.otp_attempts = 0
    user.email_verified = True
    db.commit()
    db.refresh(user)
    return user


def generate_tokens_for_user(user: Account) -> dict:
    """Generate access and refresh tokens for user"""
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    return {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "accessExpireIn": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refreshExpireIn": settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    }


def update_user_profile(
    db: Session,
    user_id: int,
    full_name: str = None,
    phone_number: str = None,
    avatar_url: str = None,
    address: str = None
) -> Account:
    """Update user profile"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    if full_name is not None:
        user.full_name = full_name
    if phone_number is not None:
        user.phone_number = phone_number
    if avatar_url is not None:
        user.avatar_url = avatar_url
    if address is not None:
        user.address = address
    
    db.commit()
    db.refresh(user)
    return user