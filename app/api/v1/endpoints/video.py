import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime

from app.schemas.video import (
    VideoAnalysisRequest,
    VideoAnalysisResponse,
    PoseDetectionResult,
    HandDetectionResult,
    FaceDetectionResult
)
from app.services.video import VideoAnalysisService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/analysis", tags=["video_analysis"])

# Create upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

video_service = VideoAnalysisService()


@router.post("/upload-pose", response_model=VideoAnalysisResponse)
async def upload_and_analyze_pose(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a video or image and analyze pose
    
    Supported formats: MP4, AVI, MOV, MKV, WEBM, PNG, JPG, JPEG
    """
    try:
        # Validate file type
        allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.png', '.jpg', '.jpeg'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Supported: {allowed_extensions}"
            )
        
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Analyze pose
        analysis_result = video_service.analyze_pose(file_path)
        
        if analysis_result["status"] == "failed":
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {analysis_result.get('error')}"
            )
        
        return VideoAnalysisResponse(
            id=file_id,
            user_id=current_user.get("id") if current_user else None,
            analysis_type="pose",
            file_name=file.filename,
            results=analysis_result["results"],
            status="success",
            created_at=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-hands", response_model=VideoAnalysisResponse)
async def upload_and_analyze_hands(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a video or image and analyze hand landmarks
    
    Supported formats: MP4, AVI, MOV, MKV, WEBM, PNG, JPG, JPEG
    """
    try:
        # Validate file type
        allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.png', '.jpg', '.jpeg'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Supported: {allowed_extensions}"
            )
        
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Analyze hands
        analysis_result = video_service.analyze_hands(file_path)
        
        if analysis_result["status"] == "failed":
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {analysis_result.get('error')}"
            )
        
        return VideoAnalysisResponse(
            id=file_id,
            user_id=current_user.get("id") if current_user else None,
            analysis_type="hands",
            file_name=file.filename,
            results=analysis_result["results"],
            status="success",
            created_at=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-face", response_model=VideoAnalysisResponse)
async def upload_and_analyze_face(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a video or image and analyze face detection
    
    Supported formats: MP4, AVI, MOV, MKV, WEBM, PNG, JPG, JPEG
    """
    try:
        # Validate file type
        allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.png', '.jpg', '.jpeg'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Supported: {allowed_extensions}"
            )
        
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Analyze face
        analysis_result = video_service.analyze_face(file_path)
        
        if analysis_result["status"] == "failed":
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {analysis_result.get('error')}"
            )
        
        return VideoAnalysisResponse(
            id=file_id,
            user_id=current_user.get("id") if current_user else None,
            analysis_type="face",
            file_name=file.filename,
            results=analysis_result["results"],
            status="success",
            created_at=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Check if video analysis service is healthy"""
    return {
        "status": "ok",
        "service": "video_analysis",
        "timestamp": datetime.utcnow()
    }
