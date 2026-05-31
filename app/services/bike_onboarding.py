from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List

from app.models.bike_onboarding import BikeOnboarding
from app.schemas.bike_onboarding import (
    SkillLevelEnum,
    RidingFrequencyEnum,
    PrimaryDisciplineEnum,
    BikeMaintenanceStyleEnum,
    YearlyBudgetRangeEnum,
    BikeOnboardingResponse,
    OnboardingProgressResponse,
)


class BikeOnboardingService:
    """Service for handling bike onboarding flow"""
    
    @staticmethod
    def get_or_create_onboarding(db: Session, user_id: int) -> BikeOnboarding:
        """Get existing onboarding or create new one"""
        onboarding = db.query(BikeOnboarding).filter(
            BikeOnboarding.user_id == user_id
        ).first()
        
        if not onboarding:
            onboarding = BikeOnboarding(user_id=user_id)
            db.add(onboarding)
            db.commit()
            db.refresh(onboarding)
        
        return onboarding
    
    @staticmethod
    def update_skill_level(
        db: Session,
        user_id: int,
        skill_level: SkillLevelEnum
    ) -> BikeOnboarding:
        """Update skill level (Step 1)"""
        onboarding = BikeOnboardingService.get_or_create_onboarding(db, user_id)
        onboarding.skill_level = skill_level
        onboarding.current_step = 2
        onboarding.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(onboarding)
        return onboarding
    
    @staticmethod
    def update_riding_frequency(
        db: Session,
        user_id: int,
        riding_frequency: RidingFrequencyEnum
    ) -> BikeOnboarding:
        """Update riding frequency (Step 2)"""
        onboarding = BikeOnboardingService.get_or_create_onboarding(db, user_id)
        onboarding.riding_frequency = riding_frequency
        onboarding.current_step = 3
        onboarding.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(onboarding)
        return onboarding
    
    @staticmethod
    def update_goals(
        db: Session,
        user_id: int,
        goals: List[str]
    ) -> BikeOnboarding:
        """Update goals (Step 3)"""
        onboarding = BikeOnboardingService.get_or_create_onboarding(db, user_id)
        onboarding.goals = goals
        onboarding.current_step = 4
        onboarding.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(onboarding)
        return onboarding
    
    @staticmethod
    def update_primary_discipline(
        db: Session,
        user_id: int,
        primary_discipline: PrimaryDisciplineEnum
    ) -> BikeOnboarding:
        """Update primary discipline (Step 4)"""
        onboarding = BikeOnboardingService.get_or_create_onboarding(db, user_id)
        onboarding.primary_discipline = primary_discipline
        onboarding.current_step = 5
        onboarding.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(onboarding)
        return onboarding
    
    @staticmethod
    def update_maintenance_style(
        db: Session,
        user_id: int,
        maintenance_style: BikeMaintenanceStyleEnum
    ) -> BikeOnboarding:
        """Update bike maintenance style (Step 5)"""
        onboarding = BikeOnboardingService.get_or_create_onboarding(db, user_id)
        onboarding.maintenance_style = maintenance_style
        onboarding.current_step = 6
        onboarding.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(onboarding)
        return onboarding
    
    @staticmethod
    def update_yearly_budget(
        db: Session,
        user_id: int,
        yearly_budget: YearlyBudgetRangeEnum
    ) -> BikeOnboarding:
        """Update yearly budget (Step 6 - Final step)"""
        onboarding = BikeOnboardingService.get_or_create_onboarding(db, user_id)
        onboarding.yearly_budget = yearly_budget
        onboarding.is_completed = True
        onboarding.current_step = 6
        onboarding.completed_at = datetime.utcnow()
        onboarding.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(onboarding)
        return onboarding
    
    @staticmethod
    def complete_onboarding_all_steps(
        db: Session,
        user_id: int,
        skill_level: SkillLevelEnum,
        riding_frequency: RidingFrequencyEnum,
        goals: List[str],
        primary_discipline: PrimaryDisciplineEnum,
        maintenance_style: BikeMaintenanceStyleEnum,
        yearly_budget: YearlyBudgetRangeEnum,
    ) -> BikeOnboarding:
        """Complete entire onboarding in one request"""
        onboarding = BikeOnboardingService.get_or_create_onboarding(db, user_id)
        onboarding.skill_level = skill_level
        onboarding.riding_frequency = riding_frequency
        onboarding.goals = goals
        onboarding.primary_discipline = primary_discipline
        onboarding.maintenance_style = maintenance_style
        onboarding.yearly_budget = yearly_budget
        onboarding.is_completed = True
        onboarding.current_step = 6
        onboarding.completed_at = datetime.utcnow()
        onboarding.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(onboarding)
        return onboarding
    
    @staticmethod
    def get_onboarding(db: Session, user_id: int) -> Optional[BikeOnboarding]:
        """Get user's onboarding data"""
        return db.query(BikeOnboarding).filter(
            BikeOnboarding.user_id == user_id
        ).first()
    
    @staticmethod
    def get_onboarding_progress(
        db: Session,
        user_id: int
    ) -> OnboardingProgressResponse:
        """Get onboarding progress"""
        onboarding = BikeOnboardingService.get_onboarding(db, user_id)
        
        if not onboarding:
            return OnboardingProgressResponse(
                user_id=user_id,
                current_step=1,
                is_completed=False,
                progress_percentage=0.0,
                total_steps=6,
                completed_steps=[]
            )
        
        # Calculate completed steps
        completed_steps = []
        if onboarding.skill_level:
            completed_steps.append(1)
        if onboarding.riding_frequency:
            completed_steps.append(2)
        if onboarding.goals:
            completed_steps.append(3)
        if onboarding.primary_discipline:
            completed_steps.append(4)
        if onboarding.maintenance_style:
            completed_steps.append(5)
        if onboarding.yearly_budget:
            completed_steps.append(6)
        
        progress_percentage = (len(completed_steps) / 6) * 100
        
        return OnboardingProgressResponse(
            user_id=user_id,
            current_step=onboarding.current_step,
            is_completed=onboarding.is_completed,
            progress_percentage=progress_percentage,
            total_steps=6,
            completed_steps=completed_steps
        )
    
    @staticmethod
    def reset_onboarding(db: Session, user_id: int) -> BikeOnboarding:
        """Reset onboarding to start from beginning"""
        onboarding = BikeOnboardingService.get_or_create_onboarding(db, user_id)
        onboarding.skill_level = None
        onboarding.riding_frequency = None
        onboarding.goals = None
        onboarding.primary_discipline = None
        onboarding.maintenance_style = None
        onboarding.yearly_budget = None
        onboarding.is_completed = False
        onboarding.current_step = 1
        onboarding.completed_at = None
        onboarding.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(onboarding)
        return onboarding
    
    @staticmethod
    def skip_step(db: Session, user_id: int) -> BikeOnboarding:
        """Skip current step and move to next"""
        onboarding = BikeOnboardingService.get_or_create_onboarding(db, user_id)
        if onboarding.current_step < 6:
            onboarding.current_step += 1
        onboarding.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(onboarding)
        return onboarding
