# API Document

## Authentication API
### 1. Register User
**POST** `/api/auth/register/`

Register a new user account.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123",
    "username": "username"
}
```

**Response:**
```json
{
    "message": "User registered successfully",
    "token": "jwt_token_here",
    "user": {
        "id": 1,
        "username": "user",
        "email": "user@example.com",
        "role": "customer",
        "salon_id": null,
        "created_at": "2024-12-19T10:00:00"
    }
}
```

### 2. Login User
**POST** `/api/auth/login/`

Login with email and password.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

### 3. Get Current User
**GET** `/api/auth/me/`

Get current user information (requires authentication).

**Headers:**
```
Authorization: Bearer <token>
```

### 4. Refresh Token
**POST** `/api/auth/refresh/`


### 5. Change Password
**POST** `/api/auth/change-password/`

### 6. Logout
**POST** `/api/auth/logout/`


## Chatbot API
```bash
# set openai api key or gemini api key or both before running this script
# export OPENAI_API_KEY=
# export GEMINI_API_KEY=

export BASE="http://localhost:5000/api/chat/"


curl -X POST "$BASE" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation": [],
    "message": "Who are your staff?",
    "user_id": 1
  }'


curl -X POST "$BASE" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation": [],
    "message": "Linh Phan có dịch vụ gì?",
    "user_id": 1
  }'

# curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
#   \"conversation\": [],
#   \"message\": \"Any availability for a Gel Manicure on 2025-10-28 between 15:00 and 16:00? Any artist is fine.\"
# }"

# curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
#   \"conversation\": [],
#   \"message\": \"Is Minh Anh free for a Gel Manicure on 2025-10-28 between 15:00 and 16:00?\"
# }"


# curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
#   \"conversation\": [],
#   \"message\": \"Ngày 2025-10-29 từ 13:00 đến 15:00 có ai làm Gel-X được không?\"
# }"


# curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
#   \"conversation\": [],
#   \"message\": \"Is there an opening for Gel Manicure with French Tips on 2025-10-28 between 14:00 and 15:30?\"
# }"


# curl -X POST "$BASE" -H "Content-Type: application/json" -d '{
#   "conversation": [],
#   "message": "I want to book a Gel Manicure on 2025-10-28 from 15:00 to 16:00. Any staff is okay.",
#   "user_id": 1
# }'


# curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
#   \"conversation\": [
#     {\"role\": \"assistant\", \"content\": \"Please confirm: Service: Gel Manicure; Staff: any available; Date: 2025-10-28; Start: 15:00; End: 16:00. Shall I book it?\"}
#   ],
#   \"message\": \"Yes, please confirm the booking.\",
#   \"user_id\": 1
# }"


# curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
#   \"conversation\": [],
#   \"message\": \"Book Gel Manicure on 2025-10-28 15:00–16:00 with Minh Anh if available, otherwise anyone.\",
#   \"user_id\": 1
# }"


# curl -X POST "$BASE" -H "Content-Type: application/json" -d '{
#   "conversation": [],
#   "message": "I’d like Gel-X on 2025-10-29 from 13:00 to 15:00. Any artist is OK."
# }'

curl -X POST "$BASE" -H "Content-Type: application/json" -d '{
  "conversation": [],
  "message": "I want to book a Gel Manicure on 2025-10-28 from 15:00 to 16:00. Any staff is okay.",
  "user_id": 1
}'



curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
  \"conversation\": [
    {\"role\": \"assistant\", \"content\": \"Please confirm: Service: Gel Manicure; Staff: Linh Phan; Date: 2025-10-28; Start: 15:00; End: 16:00. Shall I book it?\"}
  ],
  \"message\": \"Yes, please confirm the booking.\",
  \"user_id\": 1
}"

```

## Staff calendar API

### 1. Get available time slots

Get available time slots for a specific staff member on a specific date.

**Endpoint:** `GET /api/staffs/{staff_id}/available-time-slots/`

**Parameters:**
- `staff_id` (path, required): ID of the staff member
- `date` (query, required): Date in YYYY-MM-DD format

**Example Request:**
```http
GET /api/staffs/1/available-time-slots/?date=2024-01-15
```

**Success Response (200):**
```json
{
  "staff_id": 1,
  "date": "2024-01-15",
  "available_slots": ["09:00", "09:30", "10:30", "11:00", "11:30", "17:00"],
  "total_slots": 6
}
```

**Error Responses:**
- `400 Bad Request`: Missing or invalid date parameter
- `404 Not Found`: Staff member not found

**Example Error Response:**
```json
{
  "error": "Date parameter is required"
}
```

### 2. Get staff calendar by month

Get all appointments for a specific staff member with optional month and year filter.

**Endpoint:** `GET /api/staffs/{staff_id}/appointments/`

**Parameters:**
- `staff_id` (path, required): ID of the staff member
- `month` (query, optional): Month number (1-12)
- `year` (query, optional): Year (if not provided, uses current year)

**Example Requests:**
```http
GET /api/staffs/1/appointments/
GET /api/staffs/1/appointments/?month=1&year=2025
```

**Success Response (200):**
```json
{
  "staff_id": 1,
  "staff_name": "John Doe",
  "month": "1",
  "year": "2024",
  "total_appointments": 3,
  "appointments": [
    {
      "id": 1,
      "staff_id": 1,
      "user_id": 2,
      "service_id": 1,
      "phone_number": null,
      "status": "confirmed",
      "date": "2024-01-15",
      "start_time": "09:00",
      "end_time": "10:00",
      "service": {
        "id": 1,
        "name": "Haircut",
        "price": 25.0
      },
      "user": {
        "id": 2,
        "username": "jane_doe",
        "email": "jane@example.com"
      }
    }
  ]
}
```

**Error Responses:**
- `400 Bad Request`: Invalid month or year format
- `404 Not Found`: Staff member not found

**Example Error Response:**
```json
{
  "error": "Invalid month format"
}
```
