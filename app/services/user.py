"""
User service for business logic
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import SecurityUtils


class UserService:
    """Service class for user operations"""
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = UserService.get_user_by_email(db, user_create.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = UserService.get_user_by_username(db, user_create.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Hash password
        hashed_password = SecurityUtils.hash_password(user_create.password)
        
        # Create user
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
            is_active=True
        )
        
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            db.rollback()
            raise ValueError("Error creating user") from e
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
        """Update user information"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise ValueError("User not found")
        
        # Check if email is already taken by another user
        if user_update.email and user_update.email != db_user.email:
            existing = UserService.get_user_by_email(db, user_update.email)
            if existing:
                raise ValueError("Email already taken")
        
        # Check if username is already taken by another user
        if user_update.username and user_update.username != db_user.username:
            existing = UserService.get_user_by_username(db, user_update.username)
            if existing:
                raise ValueError("Username already taken")
        
        # Update fields
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def change_password(db: Session, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise ValueError("User not found")
        
        # Verify old password
        if not SecurityUtils.verify_password(old_password, db_user.hashed_password):
            raise ValueError("Incorrect password")
        
        # Hash and set new password
        db_user.hashed_password = SecurityUtils.hash_password(new_password)
        db.add(db_user)
        db.commit()
        return True
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete user (soft delete via is_active flag)"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise ValueError("User not found")
        
        db_user.is_active = False
        db.add(db_user)
        db.commit()
        return True
    
    @staticmethod
    def verify_user_password(db: Session, email: str, password: str) -> User:
        """Verify user credentials"""
        db_user = UserService.get_user_by_email(db, email)
        if not db_user:
            return None
        
        if not SecurityUtils.verify_password(password, db_user.hashed_password):
            return None
        
        if not db_user.is_active:
            return None
        
        return db_user
