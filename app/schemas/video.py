from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class AnalysisResult(BaseModel):
    """Video/Image analysis result"""
    analysis_type: str  # 'pose', 'hand', 'face', 'object_detection'
    confidence: float
    detections: List[Dict[str, Any]]
    timestamp: datetime
    

class VideoAnalysisRequest(BaseModel):
    """Request for video/image analysis"""
    analysis_type: str  # 'pose', 'hand', 'face', 'object_detection'
    description: Optional[str] = None


class VideoAnalysisResponse(BaseModel):
    """Response from video/image analysis"""
    id: str
    user_id: Optional[int] = None
    analysis_type: str
    file_name: str
    results: List[AnalysisResult]
    status: str  # 'success', 'processing', 'failed'
    created_at: datetime
    
    class Config:
        from_attributes = True


class PoseDetectionResult(BaseModel):
    """Pose detection result"""
    landmarks: List[Dict[str, float]]
    confidence: float
    frame_number: int


class HandDetectionResult(BaseModel):
    """Hand detection result"""
    hand_landmarks: List[Dict[str, float]]
    handedness: str  # 'Left' or 'Right'
    confidence: float
    frame_number: int


class FaceDetectionResult(BaseModel):
    """Face detection result"""
    face_landmarks: List[Dict[str, float]]
    confidence: float
    frame_number: int
