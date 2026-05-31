# Bike Onboarding API Documentation

Complete onboarding flow API for capturing user bike preferences and riding profile.

## Overview

The onboarding flow consists of 6 steps that guide users through setting up their bike preferences:

1. **Skill Level** - User's biking experience level
2. **Riding Frequency** - How often they ride
3. **Goals** - What they want to achieve
4. **Primary Discipline** - Type of biking they focus on
5. **Maintenance Style** - How they treat their bike
6. **Yearly Budget** - Budget for biking (Final step)

## API Endpoints

### Step-by-Step Endpoints

#### Step 1: Skill Level
**POST** `/api/v1/onboarding/step-1/skill-level`

Set user's skill level.

**Request:**
```json
{
  "skill_level": "intermediate"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "skill_level": "intermediate",
  "riding_frequency": null,
  "goals": null,
  "primary_discipline": null,
  "maintenance_style": null,
  "yearly_budget": null,
  "is_completed": false,
  "current_step": 2,
  "created_at": "2026-05-31T12:00:00",
  "updated_at": "2026-05-31T12:00:00",
  "completed_at": null
}
```

**Skill Level Options:**
- `beginner` - Just starting out
- `intermediate` - Some experience
- `advanced` - Extensive experience

---

#### Step 2: Riding Frequency
**POST** `/api/v1/onboarding/step-2/riding-frequency`

Set how often user rides.

**Request:**
```json
{
  "riding_frequency": "2-3_weeks"
}
```

**Riding Frequency Options:**
- `1-6_months` - Occasional rider
- `2-3_weeks` - Regular rider
- `daily` - Daily commuter/enthusiast

---

#### Step 3: Goals
**POST** `/api/v1/onboarding/step-3/goals`

Set user's riding goals (multiple selection).

**Request:**
```json
{
  "goals": [
    "Improve fitness",
    "Have fun with friends",
    "Commute to work"
  ]
}
```

**Example Goals:**
- Improve fitness
- Have fun with friends
- Commute to work
- Explore nature
- Racing/Competition
- Improve skills
- Mental health

---

#### Step 4: Primary Discipline
**POST** `/api/v1/onboarding/step-4/discipline`

Set primary biking discipline.

**Request:**
```json
{
  "primary_discipline": "trail"
}
```

**Primary Discipline Options:**
- `trail` - Trail biking
- `enduro` - Enduro racing
- `gravel_road` - Gravel road cycling
- `downhill_park` - Downhill park riding
- `jump_park` - Jump park/dirt jumps
- `cross_country` - Cross country racing
- `other` - Other discipline

---

#### Step 5: Bike Maintenance Style
**POST** `/api/v1/onboarding/step-5/maintenance`

Set how user treats their bike.

**Request:**
```json
{
  "maintenance_style": "for_decent"
}
```

**Maintenance Style Options:**
- `i_baby_it` - Very careful, regular maintenance
- `for_decent` - Moderate maintenance
- `i_ride_it_hard` - Aggressive riding, minimal maintenance

---

#### Step 6: Yearly Budget
**POST** `/api/v1/onboarding/step-6/budget`

Set yearly budget for biking (Final step - completes onboarding).

**Request:**
```json
{
  "yearly_budget": "750-1500"
}
```

**Yearly Budget Options:**
- `0-250` - Budget conscious
- `250-750` - Casual enthusiast
- `750-1500` - Serious enthusiast
- `1500-3000` - Professional level
- `3000+` - No budget limit

---

### Complete Onboarding (All Steps at Once)

#### Complete All Steps
**POST** `/api/v1/onboarding/complete`

Complete entire onboarding in a single request.

**Request:**
```json
{
  "skill_level": "intermediate",
  "riding_frequency": "2-3_weeks",
  "goals": ["Improve fitness", "Have fun with friends"],
  "primary_discipline": "trail",
  "maintenance_style": "for_decent",
  "yearly_budget": "750-1500"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "skill_level": "intermediate",
  "riding_frequency": "2-3_weeks",
  "goals": ["Improve fitness", "Have fun with friends"],
  "primary_discipline": "trail",
  "maintenance_style": "for_decent",
  "yearly_budget": "750-1500",
  "is_completed": true,
  "current_step": 6,
  "created_at": "2026-05-31T12:00:00",
  "updated_at": "2026-05-31T12:00:00",
  "completed_at": "2026-05-31T12:05:00"
}
```

---

### Status & Progress Endpoints

#### Get Onboarding Status
**GET** `/api/v1/onboarding/status`

Get current onboarding status and data.

**Response:**
```json
{
  "is_completed": true,
  "current_step": 6,
  "onboarding_data": {
    "id": 1,
    "user_id": 1,
    "skill_level": "intermediate",
    "riding_frequency": "2-3_weeks",
    "goals": ["Improve fitness"],
    "primary_discipline": "trail",
    "maintenance_style": "for_decent",
    "yearly_budget": "750-1500",
    "is_completed": true,
    "current_step": 6,
    "created_at": "2026-05-31T12:00:00",
    "updated_at": "2026-05-31T12:05:00",
    "completed_at": "2026-05-31T12:05:00"
  }
}
```

---

#### Get Onboarding Progress
**GET** `/api/v1/onboarding/progress`

Get onboarding progress percentage.

**Response:**
```json
{
  "user_id": 1,
  "current_step": 3,
  "is_completed": false,
  "progress_percentage": 50.0,
  "total_steps": 6,
  "completed_steps": [1, 2]
}
```

---

#### Get Onboarding Data
**GET** `/api/v1/onboarding/data`

Get complete onboarding data.

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "skill_level": "intermediate",
  "riding_frequency": "2-3_weeks",
  "goals": ["Improve fitness", "Have fun with friends"],
  "primary_discipline": "trail",
  "maintenance_style": "for_decent",
  "yearly_budget": "750-1500",
  "is_completed": true,
  "current_step": 6,
  "created_at": "2026-05-31T12:00:00",
  "updated_at": "2026-05-31T12:05:00",
  "completed_at": "2026-05-31T12:05:00"
}
```

---

### Utility Endpoints

#### Reset Onboarding
**POST** `/api/v1/onboarding/reset`

Reset onboarding to start from the beginning.

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "skill_level": null,
  "riding_frequency": null,
  "goals": null,
  "primary_discipline": null,
  "maintenance_style": null,
  "yearly_budget": null,
  "is_completed": false,
  "current_step": 1,
  "created_at": "2026-05-31T12:00:00",
  "updated_at": "2026-05-31T12:10:00",
  "completed_at": null
}
```

---

#### Skip Current Step
**POST** `/api/v1/onboarding/skip-step`

Skip current step and move to the next one.

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "skill_level": "intermediate",
  "riding_frequency": null,
  "goals": null,
  "primary_discipline": null,
  "maintenance_style": null,
  "yearly_budget": null,
  "is_completed": false,
  "current_step": 3,
  "created_at": "2026-05-31T12:00:00",
  "updated_at": "2026-05-31T12:00:00",
  "completed_at": null
}
```

---

## Authentication

All endpoints require authentication via Bearer token:

```bash
Authorization: Bearer <your_token>
```

---

## Usage Examples

### cURL Examples

**Complete entire onboarding:**
```bash
curl -X POST "http://localhost:8000/api/v1/onboarding/complete" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_level": "intermediate",
    "riding_frequency": "2-3_weeks",
    "goals": ["Improve fitness", "Have fun with friends"],
    "primary_discipline": "trail",
    "maintenance_style": "for_decent",
    "yearly_budget": "750-1500"
  }'
```

**Get progress:**
```bash
curl -X GET "http://localhost:8000/api/v1/onboarding/progress" \
  -H "Authorization: Bearer <token>"
```

**Reset onboarding:**
```bash
curl -X POST "http://localhost:8000/api/v1/onboarding/reset" \
  -H "Authorization: Bearer <token>"
```

---

### Python Example

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "your_token_here"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Complete entire onboarding
onboarding_data = {
    "skill_level": "intermediate",
    "riding_frequency": "2-3_weeks",
    "goals": ["Improve fitness", "Have fun with friends"],
    "primary_discipline": "trail",
    "maintenance_style": "for_decent",
    "yearly_budget": "750-1500"
}

response = requests.post(
    f"{BASE_URL}/onboarding/complete",
    json=onboarding_data,
    headers=headers
)

print(response.json())

# Get progress
progress = requests.get(
    f"{BASE_URL}/onboarding/progress",
    headers=headers
)

print(progress.json())
```

---

### JavaScript Example

```javascript
const BASE_URL = "http://localhost:8000/api/v1";
const token = "your_token_here";

// Complete entire onboarding
const completeOnboarding = async () => {
  const response = await fetch(`${BASE_URL}/onboarding/complete`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      skill_level: 'intermediate',
      riding_frequency: '2-3_weeks',
      goals: ['Improve fitness', 'Have fun with friends'],
      primary_discipline: 'trail',
      maintenance_style: 'for_decent',
      yearly_budget: '750-1500'
    })
  });

  const data = await response.json();
  console.log(data);
};

// Get progress
const getProgress = async () => {
  const response = await fetch(`${BASE_URL}/onboarding/progress`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  const data = await response.json();
  console.log(data);
};
```

---

## Frontend Implementation Tips

### Step-by-Step Flow
1. Start at Step 1
2. Collect user input for each step
3. Post to corresponding endpoint
4. Use `current_step` from response to navigate
5. Show progress based on `progress_percentage`
6. When `is_completed` is true, onboarding is complete

### Progressive Enhancement
- Users can skip steps using the `/skip-step` endpoint
- Users can reset and start over with `/reset` endpoint
- Users can submit all steps at once with `/complete` endpoint
- Check progress with `/progress` endpoint

### Error Handling
- 401: Unauthorized - Check token
- 404: Not found - Start onboarding first
- 500: Server error - Check server logs

---

## Database Schema

### bike_onboarding table
```
id (PRIMARY KEY)
user_id (FOREIGN KEY -> users.id, UNIQUE)
skill_level (ENUM)
riding_frequency (ENUM)
goals (JSON Array)
primary_discipline (ENUM)
maintenance_style (ENUM)
yearly_budget (ENUM)
is_completed (BOOLEAN)
current_step (INTEGER)
created_at (DATETIME)
updated_at (DATETIME)
completed_at (DATETIME)
```

---

## Implementation Files

- **Model**: `app/models/bike_onboarding.py`
- **Schemas**: `app/schemas/bike_onboarding.py`
- **Service**: `app/services/bike_onboarding.py`
- **Endpoints**: `app/api/v1/endpoints/onboarding.py`
- **Routes**: `app/api/__init__.py`

---

## Future Enhancements

- Add bike type selection
- Add location preference
- Add experience timeline
- Analytics dashboard for onboarding completion rates
- Email reminders for incomplete onboardings
- A/B testing for different onboarding flows
