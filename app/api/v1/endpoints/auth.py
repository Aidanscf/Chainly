"""
Authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.database import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
    MessageResponse
)
from app.services.user import UserService
from app.core.security import SecurityUtils
from app.core.config import settings
from app.api.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    db: Session = Depends(get_db)
) -> User:
    """
    Register a new user
    
    - **email**: User email address
    - **username**: Unique username (3-50 characters)
    - **password**: Password (minimum 8 characters)
    - **full_name**: Optional full name
    """
    try:
        user = UserService.create_user(db, user_create)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db)
) -> dict:
    """
    Login user and get access token
    
    - **email**: User email
    - **password**: User password
    
    Returns access token and refresh token
    """
    # Verify user credentials
    user = UserService.verify_user_password(db, login_request.email, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token = SecurityUtils.create_access_token(
        subject=user.id,
        additional_claims={"email": user.email, "is_superuser": user.is_superuser}
    )
    refresh_token = SecurityUtils.create_refresh_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh_token(
    refresh_request: TokenRefreshRequest,
    db: Session = Depends(get_db)
) -> dict:
    """
    Refresh access token using refresh token
    
    - **refresh_token**: Refresh token from login
    
    Returns new access token
    """
    # Decode refresh token
    payload = SecurityUtils.decode_token(refresh_request.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    user = UserService.get_user_by_id(db, int(user_id))
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token
    new_access_token = SecurityUtils.create_access_token(
        subject=user.id,
        additional_claims={"email": user.email, "is_superuser": user.is_superuser}
    )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Get current authenticated user information"""
    return current_user


@router.post("/change-password", response_model=ChangePasswordResponse)
async def change_password(
    password_change: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Change user password
    
    - **old_password**: Current password
    - **new_password**: New password (minimum 8 characters)
    """
    try:
        UserService.change_password(
            db,
            current_user.id,
            password_change.old_password,
            password_change.new_password
        )
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    Logout user (client should remove token)
    """
    return {"message": "Logged out successfully"}
