from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.bike_onboarding import (
    SkillLevelRequest,
    RidingFrequencyRequest,
    GoalsRequest,
    PrimaryDisciplineRequest,
    BikeMaintenanceStyleRequest,
    YearlyBudgetRequest,
    CompleteOnboardingRequest,
    BikeOnboardingResponse,
    OnboardingProgressResponse,
    OnboardingStatusResponse,
)
from app.services.bike_onboarding import BikeOnboardingService
from app.api.dependencies import get_current_user, get_db

router = APIRouter(prefix="/api/v1/onboarding", tags=["bike_onboarding"])


@router.post("/step-1/skill-level", response_model=BikeOnboardingResponse)
async def set_skill_level(
    request: SkillLevelRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Step 1: Set user's skill level
    
    Options:
    - beginner
    - intermediate
    - advanced
    """
    try:
        user_id = current_user.get("id")
        onboarding = BikeOnboardingService.update_skill_level(
            db, user_id, request.skill_level
        )
        return BikeOnboardingResponse.model_validate(onboarding)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/step-2/riding-frequency", response_model=BikeOnboardingResponse)
async def set_riding_frequency(
    request: RidingFrequencyRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Step 2: Set how often user rides
    
    Options:
    - 1-6_months
    - 2-3_weeks
    - daily
    """
    try:
        user_id = current_user.get("id")
        onboarding = BikeOnboardingService.update_riding_frequency(
            db, user_id, request.riding_frequency
        )
        return BikeOnboardingResponse.model_validate(onboarding)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/step-3/goals", response_model=BikeOnboardingResponse)
async def set_goals(
    request: GoalsRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Step 3: Set user's riding goals
    
    Example goals:
    - Improve fitness
    - Have fun with friends
    - Commute to work
    - Explore nature
    - Racing/Competition
    """
    try:
        user_id = current_user.get("id")
        onboarding = BikeOnboardingService.update_goals(
            db, user_id, request.goals
        )
        return BikeOnboardingResponse.model_validate(onboarding)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/step-4/discipline", response_model=BikeOnboardingResponse)
async def set_primary_discipline(
    request: PrimaryDisciplineRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Step 4: Set primary biking discipline
    
    Options:
    - trail
    - enduro
    - gravel_road
    - downhill_park
    - jump_park
    - cross_country
    - other
    """
    try:
        user_id = current_user.get("id")
        onboarding = BikeOnboardingService.update_primary_discipline(
            db, user_id, request.primary_discipline
        )
        return BikeOnboardingResponse.model_validate(onboarding)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/step-5/maintenance", response_model=BikeOnboardingResponse)
async def set_maintenance_style(
    request: BikeMaintenanceStyleRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Step 5: Set how user treats their bike
    
    Options:
    - i_baby_it (Very careful with maintenance)
    - for_decent (Moderate maintenance)
    - i_ride_it_hard (Aggressive riding style)
    """
    try:
        user_id = current_user.get("id")
        onboarding = BikeOnboardingService.update_maintenance_style(
            db, user_id, request.maintenance_style
        )
        return BikeOnboardingResponse.model_validate(onboarding)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/step-6/budget", response_model=BikeOnboardingResponse)
async def set_yearly_budget(
    request: YearlyBudgetRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Step 6: Set yearly budget for biking (Final step)
    
    Options:
    - 0-250
    - 250-750
    - 750-1500
    - 1500-3000
    - 3000+
    """
    try:
        user_id = current_user.get("id")
        onboarding = BikeOnboardingService.update_yearly_budget(
            db, user_id, request.yearly_budget
        )
        return BikeOnboardingResponse.model_validate(onboarding)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/complete", response_model=BikeOnboardingResponse)
async def complete_onboarding_all_steps(
    request: CompleteOnboardingRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Complete entire onboarding in one request (all 6 steps)
    """
    try:
        user_id = current_user.get("id")
        onboarding = BikeOnboardingService.complete_onboarding_all_steps(
            db=db,
            user_id=user_id,
            skill_level=request.skill_level,
            riding_frequency=request.riding_frequency,
            goals=request.goals,
            primary_discipline=request.primary_discipline,
            maintenance_style=request.maintenance_style,
            yearly_budget=request.yearly_budget,
        )
        return BikeOnboardingResponse.model_validate(onboarding)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/status", response_model=OnboardingStatusResponse)
async def get_onboarding_status(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current onboarding status"""
    try:
        user_id = current_user.get("id")
        onboarding = BikeOnboardingService.get_onboarding(db, user_id)
        
        if not onboarding:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Onboarding not found. Start with step 1."
            )
        
        return OnboardingStatusResponse(
            is_completed=onboarding.is_completed,
            current_step=onboarding.current_step,
            onboarding_data=BikeOnboardingResponse.model_validate(onboarding)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/progress", response_model=OnboardingProgressResponse)
async def get_onboarding_progress(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get onboarding progress"""
    try:
        user_id = current_user.get("id")
        progress = BikeOnboardingService.get_onboarding_progress(db, user_id)
        return progress
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/data", response_model=BikeOnboardingResponse)
async def get_onboarding_data(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get complete onboarding data"""
    try:
        user_id = current_user.get("id")
        onboarding = BikeOnboardingService.get_onboarding(db, user_id)
        
        if not onboarding:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No onboarding data found"
            )
        
        return BikeOnboardingResponse.model_validate(onboarding)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/reset", response_model=BikeOnboardingResponse)
async def reset_onboarding(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reset onboarding to start from beginning"""
    try:
        user_id = current_user.get("id")
        onboarding = BikeOnboardingService.reset_onboarding(db, user_id)
        return BikeOnboardingResponse.model_validate(onboarding)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/skip-step", response_model=BikeOnboardingResponse)
async def skip_current_step(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Skip current step and move to next"""
    try:
        user_id = current_user.get("id")
        onboarding = BikeOnboardingService.skip_step(db, user_id)
        return BikeOnboardingResponse.model_validate(onboarding)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
