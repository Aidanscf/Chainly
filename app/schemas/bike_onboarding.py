from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class SkillLevelEnum(str, Enum):
    """User skill level"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class RidingFrequencyEnum(str, Enum):
    """How often the user rides"""
    ONE_TO_SIX_MONTHS = "1-6_months"
    TWO_TO_THREE_WEEKS = "2-3_weeks"
    DAILY = "daily"


class PrimaryDisciplineEnum(str, Enum):
    """Primary biking discipline"""
    TRAIL = "trail"
    ENDURO = "enduro"
    GRAVEL_ROAD = "gravel_road"
    DOWNHILL_PARK = "downhill_park"
    JUMP_PARK = "jump_park"
    CROSS_COUNTRY = "cross_country"
    OTHER = "other"


class BikeMaintenanceStyleEnum(str, Enum):
    """How user treats their bike"""
    I_BABY_IT = "i_baby_it"
    FOR_DECENT = "for_decent"
    I_RIDE_IT_HARD = "i_ride_it_hard"


class YearlyBudgetRangeEnum(str, Enum):
    """Yearly budget for biking"""
    RANGE_0_250 = "0-250"
    RANGE_250_750 = "250-750"
    RANGE_750_1500 = "750-1500"
    RANGE_1500_3000 = "1500-3000"
    RANGE_3000_PLUS = "3000+"


# Step 1: Skill Level
class SkillLevelRequest(BaseModel):
    """Request for skill level step"""
    skill_level: SkillLevelEnum = Field(..., description="User's skill level")
    
    class Config:
        json_schema_extra = {
            "example": {
                "skill_level": "intermediate"
            }
        }


# Step 2: Riding Frequency
class RidingFrequencyRequest(BaseModel):
    """Request for riding frequency step"""
    riding_frequency: RidingFrequencyEnum = Field(..., description="How often user rides")
    
    class Config:
        json_schema_extra = {
            "example": {
                "riding_frequency": "2-3_weeks"
            }
        }


# Step 3: Goals
class GoalsRequest(BaseModel):
    """Request for goals step"""
    goals: List[str] = Field(..., min_items=1, description="List of user's riding goals")
    
    class Config:
        json_schema_extra = {
            "example": {
                "goals": ["Improve fitness", "Have fun with friends", "Commute to work"]
            }
        }


# Step 4: Primary Discipline
class PrimaryDisciplineRequest(BaseModel):
    """Request for primary discipline step"""
    primary_discipline: PrimaryDisciplineEnum = Field(..., description="Primary biking discipline")
    
    class Config:
        json_schema_extra = {
            "example": {
                "primary_discipline": "trail"
            }
        }


# Step 5: Bike Maintenance Style
class BikeMaintenanceStyleRequest(BaseModel):
    """Request for bike maintenance style step"""
    maintenance_style: BikeMaintenanceStyleEnum = Field(..., description="How user treats their bike")
    
    class Config:
        json_schema_extra = {
            "example": {
                "maintenance_style": "i_baby_it"
            }
        }


# Step 6: Yearly Budget
class YearlyBudgetRequest(BaseModel):
    """Request for yearly budget step"""
    yearly_budget: YearlyBudgetRangeEnum = Field(..., description="Yearly budget for biking")
    
    class Config:
        json_schema_extra = {
            "example": {
                "yearly_budget": "750-1500"
            }
        }


# Complete Onboarding
class CompleteOnboardingRequest(BaseModel):
    """Request to complete entire onboarding in one step"""
    skill_level: SkillLevelEnum
    riding_frequency: RidingFrequencyEnum
    goals: List[str] = Field(..., min_items=1)
    primary_discipline: PrimaryDisciplineEnum
    maintenance_style: BikeMaintenanceStyleEnum
    yearly_budget: YearlyBudgetRangeEnum
    
    class Config:
        json_schema_extra = {
            "example": {
                "skill_level": "intermediate",
                "riding_frequency": "2-3_weeks",
                "goals": ["Improve fitness", "Have fun"],
                "primary_discipline": "trail",
                "maintenance_style": "for_decent",
                "yearly_budget": "750-1500"
            }
        }


# Response Models
class BikeOnboardingResponse(BaseModel):
    """Response model for bike onboarding"""
    id: int
    user_id: int
    skill_level: Optional[SkillLevelEnum] = None
    riding_frequency: Optional[RidingFrequencyEnum] = None
    goals: Optional[List[str]] = None
    primary_discipline: Optional[PrimaryDisciplineEnum] = None
    maintenance_style: Optional[BikeMaintenanceStyleEnum] = None
    yearly_budget: Optional[YearlyBudgetRangeEnum] = None
    is_completed: bool
    current_step: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class OnboardingProgressResponse(BaseModel):
    """Response for onboarding progress"""
    user_id: int
    current_step: int
    is_completed: bool
    progress_percentage: float = Field(..., description="Completion percentage 0-100")
    total_steps: int = 6
    completed_steps: List[int] = Field(..., description="List of completed step numbers")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "current_step": 3,
                "is_completed": False,
                "progress_percentage": 50.0,
                "total_steps": 6,
                "completed_steps": [1, 2]
            }
        }


class OnboardingStatusResponse(BaseModel):
    """Response for onboarding status"""
    is_completed: bool
    current_step: int
    onboarding_data: BikeOnboardingResponse
