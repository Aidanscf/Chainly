import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict, Any, Optional
import os
from datetime import datetime


class VideoAnalysisService:
    """Service for video and image analysis using MediaPipe"""
    
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        
    def analyze_pose(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze pose in video or image using MediaPipe Pose
        
        Args:
            file_path: Path to video or image file
            
        Returns:
            Dictionary containing pose detection results
        """
        results_list = []
        
        try:
            # Check if file is video or image
            if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                results_list = self._analyze_video_pose(file_path)
            else:
                results_list = self._analyze_image_pose(file_path)
                
            return {
                "status": "success",
                "analysis_type": "pose",
                "results": results_list,
                "timestamp": datetime.utcnow()
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow()
            }
    
    def analyze_hands(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze hand landmarks in video or image
        
        Args:
            file_path: Path to video or image file
            
        Returns:
            Dictionary containing hand detection results
        """
        results_list = []
        
        try:
            if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                results_list = self._analyze_video_hands(file_path)
            else:
                results_list = self._analyze_image_hands(file_path)
                
            return {
                "status": "success",
                "analysis_type": "hands",
                "results": results_list,
                "timestamp": datetime.utcnow()
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow()
            }
    
    def analyze_face(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze face detection in video or image
        
        Args:
            file_path: Path to video or image file
            
        Returns:
            Dictionary containing face detection results
        """
        results_list = []
        
        try:
            if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                results_list = self._analyze_video_face(file_path)
            else:
                results_list = self._analyze_image_face(file_path)
                
            return {
                "status": "success",
                "analysis_type": "face",
                "results": results_list,
                "timestamp": datetime.utcnow()
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow()
            }
    
    def _analyze_image_pose(self, image_path: str) -> List[Dict[str, Any]]:
        """Analyze pose in a single image"""
        image = cv2.imread(image_path)
        results = []
        
        with self.mp_pose.Pose(static_image_mode=True) as pose:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pose_results = pose.process(image_rgb)
            
            if pose_results.pose_landmarks:
                landmarks = self._extract_landmarks(pose_results.pose_landmarks)
                results.append({
                    "landmarks": landmarks,
                    "confidence": 0.95,
                    "frame_number": 0
                })
        
        return results
    
    def _analyze_video_pose(self, video_path: str) -> List[Dict[str, Any]]:
        """Analyze pose in a video"""
        cap = cv2.VideoCapture(video_path)
        results = []
        frame_count = 0
        
        with self.mp_pose.Pose() as pose:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pose_results = pose.process(image_rgb)
                
                if pose_results.pose_landmarks:
                    landmarks = self._extract_landmarks(pose_results.pose_landmarks)
                    results.append({
                        "landmarks": landmarks,
                        "confidence": 0.95,
                        "frame_number": frame_count
                    })
                
                frame_count += 1
                
                # Limit frames for performance
                if frame_count > 300:
                    break
        
        cap.release()
        return results
    
    def _analyze_image_hands(self, image_path: str) -> List[Dict[str, Any]]:
        """Analyze hands in a single image"""
        image = cv2.imread(image_path)
        results = []
        
        with self.mp_hands.Hands(static_image_mode=True) as hands:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            hand_results = hands.process(image_rgb)
            
            if hand_results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(
                    hand_results.multi_hand_landmarks,
                    hand_results.multi_handedness
                ):
                    landmarks = self._extract_landmarks(hand_landmarks)
                    results.append({
                        "hand_landmarks": landmarks,
                        "handedness": handedness.classification[0].label,
                        "confidence": handedness.classification[0].score,
                        "frame_number": 0
                    })
        
        return results
    
    def _analyze_video_hands(self, video_path: str) -> List[Dict[str, Any]]:
        """Analyze hands in a video"""
        cap = cv2.VideoCapture(video_path)
        results = []
        frame_count = 0
        
        with self.mp_hands.Hands() as hands:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                hand_results = hands.process(image_rgb)
                
                if hand_results.multi_hand_landmarks:
                    for hand_landmarks, handedness in zip(
                        hand_results.multi_hand_landmarks,
                        hand_results.multi_handedness
                    ):
                        landmarks = self._extract_landmarks(hand_landmarks)
                        results.append({
                            "hand_landmarks": landmarks,
                            "handedness": handedness.classification[0].label,
                            "confidence": handedness.classification[0].score,
                            "frame_number": frame_count
                        })
                
                frame_count += 1
                if frame_count > 300:
                    break
        
        cap.release()
        return results
    
    def _analyze_image_face(self, image_path: str) -> List[Dict[str, Any]]:
        """Analyze face in a single image"""
        image = cv2.imread(image_path)
        results = []
        
        with self.mp_face_detection.FaceDetection() as face_detection:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_results = face_detection.process(image_rgb)
            
            if face_results.detections:
                for detection in face_results.detections:
                    landmarks = self._extract_face_landmarks(detection)
                    results.append({
                        "landmarks": landmarks,
                        "confidence": detection.score[0],
                        "frame_number": 0
                    })
        
        return results
    
    def _analyze_video_face(self, video_path: str) -> List[Dict[str, Any]]:
        """Analyze face in a video"""
        cap = cv2.VideoCapture(video_path)
        results = []
        frame_count = 0
        
        with self.mp_face_detection.FaceDetection() as face_detection:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_results = face_detection.process(image_rgb)
                
                if face_results.detections:
                    for detection in face_results.detections:
                        landmarks = self._extract_face_landmarks(detection)
                        results.append({
                            "landmarks": landmarks,
                            "confidence": detection.score[0],
                            "frame_number": frame_count
                        })
                
                frame_count += 1
                if frame_count > 300:
                    break
        
        cap.release()
        return results
    
    def _extract_landmarks(self, landmarks) -> List[Dict[str, float]]:
        """Extract landmarks from MediaPipe format"""
        result = []
        for landmark in landmarks.landmark:
            result.append({
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z,
                "visibility": landmark.visibility
            })
        return result
    
    def _extract_face_landmarks(self, detection) -> Dict[str, Any]:
        """Extract face landmarks from detection"""
        bbox = detection.location_data.bounding_box
        return {
            "bbox": {
                "x_min": bbox.xmin,
                "y_min": bbox.ymin,
                "width": bbox.width,
                "height": bbox.height
            },
            "keypoints": [
                {"x": kp.x, "y": kp.y} 
                for kp in detection.location_data.relative_keypoints
            ]
        }
