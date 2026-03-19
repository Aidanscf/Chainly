"""
Main API router that includes all endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

# Include routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
