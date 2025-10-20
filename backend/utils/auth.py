from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
import os

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def check_subscription_status(user):
    """Check if user's subscription is active."""
    now = datetime.now()
    
    if user.subscription_status == "trial":
        if now > user.trial_end_date:
            return False, "Trial period expired"
        return True, f"Trial active until {user.trial_end_date.strftime('%Y-%m-%d')}"
    
    elif user.subscription_status == "active":
        if user.subscription_end_date and now > user.subscription_end_date:
            return False, "Subscription expired"
        return True, f"Subscription active until {user.subscription_end_date.strftime('%Y-%m-%d')}"
    
    else:
        return False, "No active subscription"

def get_patient_limit(user):
    """Get patient limit based on subscription plan."""
    limits = {
        "trial": 3,  # Trial limit
        "basic": 50,
        "professional": 200,
        "enterprise": -1  # Unlimited
    }
    
    # If user is in trial, return trial limit
    if user.subscription_status == "trial":
        return limits["trial"]
    
    return limits.get(user.subscription_plan, 3)
