from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr

from database import get_db
from models.user import User, UserRole, SubscriptionStatus, SubscriptionPlan
from utils.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    verify_token,
    check_subscription_status,
    get_patient_limit
)

router = APIRouter()
security = HTTPBearer()

# Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    professional_license: Optional[str] = None
    specialization: Optional[str] = None
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    bio: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    role: UserRole
    subscription_status: SubscriptionStatus
    subscription_plan: SubscriptionPlan
    trial_end_date: Optional[datetime]
    subscription_end_date: Optional[datetime]
    professional_license: Optional[str]
    specialization: Optional[str]
    clinic_name: Optional[str]
    clinic_address: Optional[str]
    bio: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
    subscription_info: dict

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

# Dependency to get current user
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    token = credentials.credentials
    user_id = verify_token(token)
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    
    return user

# Endpoints
@router.post("/register", response_model=TokenResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new nutritionist."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    trial_end_date = datetime.now() + timedelta(days=30)
    
    db_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        professional_license=user_data.professional_license,
        specialization=user_data.specialization,
        clinic_name=user_data.clinic_name,
        clinic_address=user_data.clinic_address,
        bio=user_data.bio,
        trial_end_date=trial_end_date
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": str(db_user.id)})
    
    # Check subscription status
    is_active, message = check_subscription_status(db_user)
    patient_limit = get_patient_limit(db_user)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=db_user,
        subscription_info={
            "is_active": is_active,
            "message": message,
            "patient_limit": patient_limit,
            "days_remaining": (db_user.trial_end_date - datetime.now()).days if db_user.trial_end_date else 0
        }
    )

@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login user."""
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    
    # Update last login
    user.last_login = datetime.now()
    db.commit()
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # Check subscription status
    is_active, message = check_subscription_status(user)
    patient_limit = get_patient_limit(user)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user,
        subscription_info={
            "is_active": is_active,
            "message": message,
            "patient_limit": patient_limit,
            "days_remaining": (user.trial_end_date - datetime.now()).days if user.trial_end_date else 0
        }
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user

@router.get("/subscription-status")
def get_subscription_status(current_user: User = Depends(get_current_user)):
    """Get subscription status and limits."""
    is_active, message = check_subscription_status(current_user)
    patient_limit = get_patient_limit(current_user)
    
    return {
        "is_active": is_active,
        "message": message,
        "patient_limit": patient_limit,
        "current_plan": current_user.subscription_plan,
        "status": current_user.subscription_status,
        "days_remaining": (current_user.trial_end_date - datetime.now()).days if current_user.trial_end_date else 0
    }

@router.post("/change-password")
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password."""
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}

@router.post("/upgrade-subscription")
def upgrade_subscription(
    plan: SubscriptionPlan,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upgrade user subscription (placeholder for payment integration)."""
    current_user.subscription_plan = plan
    current_user.subscription_status = SubscriptionStatus.active
    current_user.subscription_start_date = datetime.now()
    current_user.subscription_end_date = datetime.now() + timedelta(days=30)  # Monthly
    
    db.commit()
    
    return {
        "message": f"Subscription upgraded to {plan}",
        "new_plan": plan,
        "expires_at": current_user.subscription_end_date
    }
