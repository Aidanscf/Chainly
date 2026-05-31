from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.database import Base


class SkillLevel(str, enum.Enum):
    """User skill level"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class RidingFrequency(str, enum.Enum):
    """How often the user rides"""
    ONE_TO_SIX_MONTHS = "1-6_months"
    TWO_TO_THREE_WEEKS = "2-3_weeks"
    DAILY = "daily"


class PrimaryDiscipline(str, enum.Enum):
    """Primary biking discipline"""
    TRAIL = "trail"
    ENDURO = "enduro"
    GRAVEL_ROAD = "gravel_road"
    DOWNHILL_PARK = "downhill_park"
    JUMP_PARK = "jump_park"
    CROSS_COUNTRY = "cross_country"
    OTHER = "other"


class BikeMaintenanceStyle(str, enum.Enum):
    """How user treats their bike"""
    I_BABY_IT = "i_baby_it"
    FOR_DECENT = "for_decent"
    I_RIDE_IT_HARD = "i_ride_it_hard"


class YearlyBudgetRange(str, enum.Enum):
    """Yearly budget for biking"""
    RANGE_0_250 = "0-250"
    RANGE_250_750 = "250-750"
    RANGE_750_1500 = "750-1500"
    RANGE_1500_3000 = "1500-3000"
    RANGE_3000_PLUS = "3000+"


class BikeOnboarding(Base):
    """User bike onboarding preferences"""
    __tablename__ = "bike_onboarding"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False, index=True)
    
    # Step 1: Skill Level
    skill_level = Column(Enum(SkillLevel), nullable=True)
    
    # Step 2: Riding Frequency
    riding_frequency = Column(Enum(RidingFrequency), nullable=True)
    
    # Step 3: Goals (multiple selections stored as JSON)
    goals = Column(JSON, nullable=True)  # List of goal strings
    
    # Step 4: Primary Discipline
    primary_discipline = Column(Enum(PrimaryDiscipline), nullable=True)
    
    # Step 5: Bike Maintenance Style
    maintenance_style = Column(Enum(BikeMaintenanceStyle), nullable=True)
    
    # Step 6: Yearly Spend on Biking
    yearly_budget = Column(Enum(YearlyBudgetRange), nullable=True)
    
    # Completion tracking
    is_completed = Column(Boolean, default=False)
    current_step = Column(Integer, default=1)  # Track which step user is on
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="bike_onboarding")
    
    def __repr__(self):
        return f"<BikeOnboarding(user_id={self.user_id}, step={self.current_step}, completed={self.is_completed})>"
