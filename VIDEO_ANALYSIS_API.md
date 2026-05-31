# Video and Image Analysis API

This API provides endpoints for uploading and analyzing videos and images using MediaPipe for pose detection, hand detection, and face detection.

## Features

- **Pose Detection**: Detect and track body pose/skeletal landmarks
- **Hand Detection**: Detect hand landmarks and handedness (left/right)
- **Face Detection**: Detect faces and facial landmarks
- **Multi-format Support**: Supports video (MP4, AVI, MOV, MKV, WEBM) and image formats (PNG, JPG, JPEG)

## Installation

MediaPipe has already been added to `requirements.txt`. Install dependencies:

```bash
pip install -r requirements.txt
```

## API Endpoints

### 1. Pose Detection
**Endpoint**: `POST /api/v1/analysis/upload-pose`

Upload a video or image to analyze pose/skeletal landmarks.

**Request**:
- `file`: UploadFile (required) - Video or image file
- `description`: String (optional) - Description of the analysis

**Response**:
```json
{
  "id": "uuid",
  "user_id": 123,
  "analysis_type": "pose",
  "file_name": "video.mp4",
  "results": [
    {
      "landmarks": [
        {
          "x": 0.5,
          "y": 0.3,
          "z": 0.1,
          "visibility": 0.95
        }
      ],
      "confidence": 0.95,
      "frame_number": 0
    }
  ],
  "status": "success",
  "created_at": "2026-05-31T12:00:00"
}
```

### 2. Hand Detection
**Endpoint**: `POST /api/v1/analysis/upload-hands`

Upload a video or image to analyze hand landmarks.

**Request**:
- `file`: UploadFile (required) - Video or image file
- `description`: String (optional) - Description of the analysis

**Response**:
```json
{
  "id": "uuid",
  "user_id": 123,
  "analysis_type": "hands",
  "file_name": "image.jpg",
  "results": [
    {
      "hand_landmarks": [
        {
          "x": 0.5,
          "y": 0.3,
          "z": 0.1,
          "visibility": 0.95
        }
      ],
      "handedness": "Right",
      "confidence": 0.98,
      "frame_number": 0
    }
  ],
  "status": "success",
  "created_at": "2026-05-31T12:00:00"
}
```

### 3. Face Detection
**Endpoint**: `POST /api/v1/analysis/upload-face`

Upload a video or image to analyze face detection.

**Request**:
- `file`: UploadFile (required) - Video or image file
- `description`: String (optional) - Description of the analysis

**Response**:
```json
{
  "id": "uuid",
  "user_id": 123,
  "analysis_type": "face",
  "file_name": "video.mp4",
  "results": [
    {
      "landmarks": {
        "bbox": {
          "x_min": 0.2,
          "y_min": 0.1,
          "width": 0.3,
          "height": 0.4
        },
        "keypoints": [
          {
            "x": 0.35,
            "y": 0.25
          }
        ]
      },
      "confidence": 0.92,
      "frame_number": 0
    }
  ],
  "status": "success",
  "created_at": "2026-05-31T12:00:00"
}
```

### 4. Health Check
**Endpoint**: `GET /api/v1/analysis/health`

Check if the video analysis service is running.

**Response**:
```json
{
  "status": "ok",
  "service": "video_analysis",
  "timestamp": "2026-05-31T12:00:00"
}
```

## Authentication

All endpoints require authentication. Pass your authentication token in the `Authorization` header:

```bash
Authorization: Bearer <your_token>
```

## Usage Examples

### Using cURL

**Pose Detection**:
```bash
curl -X POST "http://localhost:8000/api/v1/analysis/upload-pose" \
  -H "Authorization: Bearer <token>" \
  -F "file=@video.mp4" \
  -F "description=My fitness video"
```

**Hand Detection**:
```bash
curl -X POST "http://localhost:8000/api/v1/analysis/upload-hands" \
  -H "Authorization: Bearer <token>" \
  -F "file=@hands.jpg"
```

**Face Detection**:
```bash
curl -X POST "http://localhost:8000/api/v1/analysis/upload-face" \
  -H "Authorization: Bearer <token>" \
  -F "file=@face.mp4"
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/api/v1/analysis/upload-pose"
headers = {"Authorization": "Bearer <token>"}
files = {"file": open("video.mp4", "rb")}
data = {"description": "My fitness video"}

response = requests.post(url, headers=headers, files=files, data=data)
print(response.json())
```

### Using JavaScript fetch

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('description', 'My fitness video');

const response = await fetch('http://localhost:8000/api/v1/analysis/upload-pose', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer <token>'
  },
  body: formData
});

const result = await response.json();
console.log(result);
```

## File Size Limits

- Maximum file size: Limited by server configuration (default: 100MB)
- Video duration analyzed: First 300 frames for performance

## Supported Formats

**Video**:
- MP4
- AVI
- MOV
- MKV
- WEBM

**Images**:
- PNG
- JPG
- JPEG

## Output Explanation

### Landmarks
Each landmark contains:
- `x`: Horizontal coordinate (0.0-1.0, relative to image width)
- `y`: Vertical coordinate (0.0-1.0, relative to image height)
- `z`: Depth coordinate (0.0-1.0, relative to shoulder width)
- `visibility`: Confidence score for landmark visibility (0.0-1.0)

### Frame Information
- For images: `frame_number` is always 0
- For videos: `frame_number` indicates the frame position in the video

## Error Handling

Error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common errors:
- **400**: Unsupported file format
- **401**: Unauthorized (missing/invalid token)
- **500**: Server error during analysis

## Performance Considerations

- **Video analysis**: Analyzes up to 300 frames per video for performance
- **Large files**: Videos larger than 1GB may take longer to process
- **Concurrent requests**: Handle multiple requests efficiently with async processing

## Implementation Files

- **Schema**: `app/schemas/video.py` - Data models for requests/responses
- **Service**: `app/services/video.py` - MediaPipe analysis logic
- **Endpoints**: `app/api/v1/endpoints/video.py` - API route handlers
- **Router**: `app/api/__init__.py` - Route registration

## Future Enhancements

- Support for custom MediaPipe solutions
- Real-time WebSocket analysis
- Batch analysis for multiple files
- Results storage in database
- Advanced filtering and post-processing options
