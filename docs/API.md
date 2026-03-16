# Speed Up API Documentation

## Table of Contents
- [Speed Up API Documentation](#speed-up-api-documentation)
  - [Table of Contents](#table-of-contents)
  - [Authentication](#authentication)
    - [Overview](#overview)
    - [Authorization Header](#authorization-header)
  - [Auth](#auth)
    - [POST /api/auth/signup](#post-apiauthsignup)
    - [POST /api/auth/login](#post-apiauthlogin)
    - [POST /api/auth/refresh](#post-apiauthrefresh)
    - [POST /api/auth/logout](#post-apiauthlogout)
    - [POST /api/auth/otp/verify](#post-apiauthotpverify)
    - [POST /api/auth/otp/resend](#post-apiauthotpresend)
    - [POST /api/auth/otp/send](#post-apiauthotpsend)
    - [POST /api/auth/email/otp/verify](#post-apiauthemailotpverify)
    - [GET /api/auth/profile](#get-apiauthprofile)
    - [PUT /api/auth/profile](#put-apiauthprofile)
    - [POST /api/auth/subscription](#post-apiauthsubscription)
  - [Content - Grades](#content---grades)
    - [GET /api/content/grades](#get-apicontentgrades)
    - [GET /api/content/grades/{grade\_id}](#get-apicontentgradesgrade_id)
  - [Content - Topics](#content---topics)
    - [GET /api/content/topics](#get-apicontenttopics)
    - [GET /api/content/grades/{grade\_id}/topics](#get-apicontentgradesgrade_idtopics)
    - [GET /api/content/topics/{topic\_id}](#get-apicontenttopicstopic_id)
  - [Content - Specializations](#content---specializations)
    - [GET /api/content/specializations](#get-apicontentspecializations)
    - [GET /api/content/topics/{topic\_id}/specializations](#get-apicontenttopicstopic_idspecializations)
    - [GET /api/content/specializations/{specialization\_id}](#get-apicontentspecializationsspecialization_id)
  - [Content - Exercises](#content---exercises)
    - [GET /api/content/exercises](#get-apicontentexercises)
    - [GET /api/content/specializations/{specialization\_id}/exercises](#get-apicontentspecializationsspecialization_idexercises)
    - [GET /api/content/specializations/{specialization\_id}/exercises/difficulty/{difficulty}](#get-apicontentspecializationsspecialization_idexercisesdifficultydifficulty)
    - [GET /api/content/exercises/{exercise\_id}](#get-apicontentexercisesexercise_id)
  - [Content - Exam](#content---exam)
    - [GET /api/content/exercises/{exercise\_id}/exam](#get-apicontentexercisesexercise_idexam)
  - [Content - Exam Submission \& History](#content---exam-submission--history)
    - [POST /api/content/exam/submit](#post-apicontentexamsubmit)
    - [GET /api/content/exam/history](#get-apicontentexamhistory)
    - [GET /api/content/exam/history/exercise/{exercise\_id}](#get-apicontentexamhistoryexerciseexercise_id)
    - [GET /api/content/exam/attempts/{attempt\_id}](#get-apicontentexamattemptsattempt_id)
  - [Content - Questions](#content---questions)
    - [GET /api/content/exercises/{exercise\_id}/questions](#get-apicontentexercisesexercise_idquestions)
    - [GET /api/content/exercises/{exercise\_id}/questions-with-options](#get-apicontentexercisesexercise_idquestions-with-options)
    - [GET /api/content/questions/{question\_id}](#get-apicontentquestionsquestion_id)
    - [GET /api/content/questions/{question\_id}/options](#get-apicontentquestionsquestion_idoptions)
  - [Admin - Dashboard](#admin---dashboard)
    - [GET /api/admin/dashboard](#get-apiadmindashboard)
    - [GET /api/admin/stats/exercises](#get-apiadminstatsexercises)
    - [GET /api/admin/stats/users](#get-apiadminstatsusers)
  - [Admin - User Management](#admin---user-management)
    - [GET /api/admin/users](#get-apiadminusers)
    - [GET /api/admin/users/{user\_id}](#get-apiadminusersuser_id)
    - [PUT /api/admin/users/{user\_id}](#put-apiadminusersuser_id)
    - [PATCH /api/admin/users/{user\_id}/deactivate](#patch-apiadminusersuser_iddeactivate)
    - [PATCH /api/admin/users/{user\_id}/activate](#patch-apiadminusersuser_idactivate)
  - [Admin - Grade Management](#admin---grade-management)
    - [POST /api/admin/grades](#post-apiadmingrades)
    - [PUT /api/admin/grades/{grade\_id}](#put-apiadmingradesgrade_id)
    - [DELETE /api/admin/grades/{grade\_id}](#delete-apiadmingradesgrade_id)
  - [Admin - Topic Management](#admin---topic-management)
    - [POST /api/admin/topics](#post-apiadmintopics)
    - [PUT /api/admin/topics/{topic\_id}](#put-apiadmintopicstopic_id)
    - [DELETE /api/admin/topics/{topic\_id}](#delete-apiadmintopicstopic_id)
  - [Admin - Specialization Management](#admin---specialization-management)
    - [POST /api/admin/specializations](#post-apiadminspecializations)
    - [PUT /api/admin/specializations/{specialization\_id}](#put-apiadminspecializationsspecialization_id)
    - [DELETE /api/admin/specializations/{specialization\_id}](#delete-apiadminspecializationsspecialization_id)
  - [Admin - Exercise Management](#admin---exercise-management)
    - [POST /api/admin/exercises](#post-apiadminexercises)
    - [PUT /api/admin/exercises/{exercise\_id}](#put-apiadminexercisesexercise_id)
    - [DELETE /api/admin/exercises/{exercise\_id}](#delete-apiadminexercisesexercise_id)
  - [Admin - Question Management](#admin---question-management)
    - [POST /api/admin/questions](#post-apiadminquestions)
    - [PUT /api/admin/questions/{question\_id}](#put-apiadminquestionsquestion_id)
    - [DELETE /api/admin/questions/{question\_id}](#delete-apiadminquestionsquestion_id)
  - [Error Codes](#error-codes)
  - [Database Schema](#database-schema)
    - [Tables](#tables)
    - [Hierarchy](#hierarchy)

---

## Authentication

### Overview
This API uses JWT (JSON Web Token) for authentication:
- **Access Token**: Short-lived (30 minutes) for API access
- **Refresh Token**: Long-lived (7 days) for token rotation

### Authorization Header
```
Authorization: Bearer <access_token>
```

---

## Auth

### POST /api/auth/signup

**Register a new user and return tokens. If user exists but not verified, will resend OTP.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | POST | `/api/auth/signup` |

**Request:**
```json
{
  "email": "string",
  "password": "string",
  "fullName": "string"
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "accessToken": "string",
    "refreshToken": "string",
    "accessExpireIn": 1800,
    "refreshExpireIn": 604800
  }
}
```

---

### POST /api/auth/login

**Authenticate with email and password.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | POST | `/api/auth/login` |

**Request:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "accessToken": "string",
    "refreshToken": "string",
    "accessExpireIn": 1800,
    "refreshExpireIn": 604800
  }
}
```

---

### POST /api/auth/refresh

**Rotate refresh token and return a new token pair.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | POST | `/api/auth/refresh` |

**Request:**
```json
{
  "refreshToken": "string"
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "accessToken": "string",
    "refreshToken": "string",
    "accessExpireIn": 1800,
    "refreshExpireIn": 604800
  }
}
```

---

### POST /api/auth/logout

**Revoke refresh token.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | POST | `/api/auth/logout` |

**Request:**
```json
{
  "refreshToken": "string"
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": null
}
```

---

### POST /api/auth/otp/verify

**Verify OTP and activate account (without authentication).**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | POST | `/api/auth/otp/verify` |

**Request:**
```json
{
  "email": "string",
  "otp": "string"
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "accessToken": "string",
    "refreshToken": "string",
    "accessExpireIn": 1800,
    "refreshExpireIn": 604800
  }
}
```

---

### POST /api/auth/otp/resend

**Resend OTP to email (without authentication). User must exist and not be verified yet.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | POST | `/api/auth/otp/resend` |

**Request:**
```json
{
  "email": "string"
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": null
}
```

---

### POST /api/auth/otp/send

**Send a verification OTP to the authenticated user's email. OTP TTL: 10 minutes.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token | POST | `/api/auth/otp/send` |

**Response (Success):**
```json
{
  "success": true,
  "data": null
}
```

---

### POST /api/auth/email/otp/verify

**Verify OTP for authenticated user and issue new tokens. Max 5 attempts.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token | POST | `/api/auth/email/otp/verify` |

**Request:**
```json
{
  "otp": "string"
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "accessToken": "string",
    "refreshToken": "string",
    "accessExpireIn": 1800,
    "refreshExpireIn": 604800
  }
}
```

---

### GET /api/auth/profile

**Get current user's profile.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token | GET | `/api/auth/profile` |

**Response (Success):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "fullName": "Nguyen Van A",
  "phoneNumber": "0123456789",
  "avatarUrl": "https://...",
  "address": "Ha Noi",
  "role": "student",
  "emailVerified": true,
  "subscriptionType": "plus",
  "subscriptionStart": "2026-02-28T00:00:00",
  "subscriptionEnd": "2026-03-28T00:00:00",
  "isActive": true
}
```

---

### PUT /api/auth/profile

**Update current user's profile.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token | PUT | `/api/auth/profile` |

**Request:**
```json
{
  "fullName": "string",
  "phoneNumber": "string",
  "avatarUrl": "string",
  "address": "string"
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": null
}
```

---

### POST /api/auth/subscription

**Subscribe to premium plan (plus: 1 month, pro: 3 months, vip: 6 months, max: 12 months).**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token | POST | `/api/auth/subscription` |

**Request:**
```json
{
  "subscription_type": "plus"
}
```

**Plans:**
- `plus`: 1 month
- `pro`: 3 months
- `vip`: 6 months
- `max`: 12 months

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "subscriptionType": "plus",
    "subscriptionStart": "2026-03-05T00:00:00",
    "subscriptionEnd": "2026-04-04T00:00:00",
    "isActive": true
  }
}
```

---

## Content - Grades

### GET /api/content/grades

**Lấy tất cả các lớp.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/grades` |

**Response:**
```json
{
  "grades": [
    { "id": 10, "name": "Lớp 10", "description": "Chương trình Vật Lý Lớp 10" },
    { "id": 11, "name": "Lớp 11", "description": "Chương trình Vật Lý Lớp 11" },
    { "id": 12, "name": "Lớp 12", "description": "Chương trình Vật Lý Lớp 12" }
  ]
}
```

---

### GET /api/content/grades/{grade_id}

**Lấy thông tin lớp theo ID.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/grades/{grade_id}` |

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| grade_id  | int  | Yes      | ID của lớp  |

**Response:**
```json
{
  "id": 10,
  "name": "Lớp 10",
  "description": "Chương trình Vật Lý Lớp 10"
}
```

---

## Content - Topics

### GET /api/content/topics

**Lấy tất cả chương (topics) trong hệ thống.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/topics` |

**Response:**
```json
{
  "topics": [
    {
      "id": 101,
      "grade_id": 10,
      "name": "Chương 1: Mở đầu",
      "description": null,
      "created_at": "2026-02-28T00:00:00"
    }
  ]
}
```

---

### GET /api/content/grades/{grade_id}/topics

**Lấy danh sách chương theo lớp.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/grades/{grade_id}/topics` |

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| grade_id  | int  | Yes      | ID của lớp  |

**Response:**
```json
{
  "topics": [
    {
      "id": 101,
      "grade_id": 10,
      "name": "Chương 1: Mở đầu",
      "description": null,
      "created_at": "2026-02-28T00:00:00"
    },
    {
      "id": 102,
      "grade_id": 10,
      "name": "Chương 2: Động học",
      "description": null,
      "created_at": "2026-02-28T00:00:00"
    }
  ]
}
```

---

### GET /api/content/topics/{topic_id}

**Lấy thông tin chương theo ID.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/topics/{topic_id}` |

| Parameter | Type | Required | Description    |
|-----------|------|----------|----------------|
| topic_id  | int  | Yes      | ID của chương  |

**Response:**
```json
{
  "id": 101,
  "grade_id": 10,
  "name": "Chương 1: Mở đầu",
  "description": null,
  "created_at": "2026-02-28T00:00:00"
}
```

---

## Content - Specializations

### GET /api/content/specializations

**Lấy tất cả chuyên đề.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/specializations` |

**Response:**
```json
{
  "specializations": [
    {
      "id": 1,
      "topic_id": 101,
      "name": "Bài 1: Làm quen với Vật Lý",
      "description": null,
      "order_index": 1,
      "created_by": null,
      "created_at": "2026-02-28T00:00:00"
    }
  ]
}
```

---

### GET /api/content/topics/{topic_id}/specializations

**Lấy danh sách chuyên đề theo chương.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/topics/{topic_id}/specializations` |

| Parameter | Type | Required | Description    |
|-----------|------|----------|----------------|
| topic_id  | int  | Yes      | ID của chương  |

**Response:**
```json
{
  "specializations": [
    {
      "id": 1,
      "topic_id": 101,
      "name": "Bài 1: Làm quen với Vật Lý",
      "description": null,
      "order_index": 1,
      "created_by": null,
      "created_at": "2026-02-28T00:00:00"
    },
    {
      "id": 2,
      "topic_id": 101,
      "name": "Bài 2: Các quy tắc an toàn trong phòng thực hành Vật Lý",
      "description": null,
      "order_index": 2,
      "created_by": null,
      "created_at": "2026-02-28T00:00:00"
    }
  ]
}
```

---

### GET /api/content/specializations/{specialization_id}

**Lấy thông tin chuyên đề theo ID.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/specializations/{specialization_id}` |

| Parameter         | Type | Required | Description         |
|-------------------|------|----------|---------------------|
| specialization_id | int  | Yes      | ID của chuyên đề    |

**Response:**
```json
{
  "id": 1,
  "topic_id": 101,
  "name": "Bài 1: Làm quen với Vật Lý",
  "description": null,
  "order_index": 1,
  "created_by": null,
  "created_at": "2026-02-28T00:00:00"
}
```

---

## Content - Exercises

### GET /api/content/exercises

**Lấy tất cả bài kiểm tra.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/exercises` |

**Response:**
```json
{
  "exercises": [
    {
      "id": 1,
      "specialization_id": 1,
      "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
      "difficulty_level": "easy",
      "duration": 45,
      "created_by": null,
      "created_at": "2026-02-28T00:00:00"
    }
  ]
}
```

---

### GET /api/content/specializations/{specialization_id}/exercises

**Lấy danh sách bài kiểm tra theo chuyên đề.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/specializations/{specialization_id}/exercises` |

| Parameter         | Type | Required | Description         |
|-------------------|------|----------|---------------------|
| specialization_id | int  | Yes      | ID của chuyên đề    |

**Response:**
```json
{
  "exercises": [
    {
      "id": 1,
      "specialization_id": 1,
      "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
      "difficulty_level": "easy",
      "duration": 45,
      "created_by": null,
      "created_at": "2026-02-28T00:00:00"
    }
  ]
}
```

---

### GET /api/content/specializations/{specialization_id}/exercises/difficulty/{difficulty}

**Lấy bài kiểm tra theo độ khó.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/specializations/{specialization_id}/exercises/difficulty/{difficulty}` |

| Parameter         | Type   | Required | Description                            |
|-------------------|--------|----------|----------------------------------------|
| specialization_id | int    | Yes      | ID của chuyên đề                       |
| difficulty        | string | Yes      | Độ khó: `easy`, `medium`, `hard`, `expert` |

**Response:**
```json
{
  "exercises": [
    {
      "id": 1,
      "specialization_id": 1,
      "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
      "difficulty_level": "easy",
      "duration": 45,
      "created_by": null,
      "created_at": "2026-02-28T00:00:00"
    }
  ]
}
```

---

### GET /api/content/exercises/{exercise_id}

**Lấy thông tin bài kiểm tra theo ID.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/exercises/{exercise_id}` |

| Parameter   | Type | Required | Description             |
|-------------|------|----------|-------------------------|
| exercise_id | int  | Yes      | ID của bài kiểm tra     |

**Response:**
```json
{
  "id": 1,
  "specialization_id": 1,
  "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
  "difficulty_level": "easy",
  "duration": 45,
  "created_by": null,
  "created_at": "2026-02-28T00:00:00"
}
```

---

## Content - Exam

### GET /api/content/exercises/{exercise_id}/exam

**Lấy đầy đủ bài thi: thông tin bài kiểm tra + tất cả câu hỏi + đáp án. Dùng để tạo bài thi cho học sinh.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/exercises/{exercise_id}/exam` |

| Parameter   | Type | Required | Description             |
|-------------|------|----------|-------------------------|
| exercise_id | int  | Yes      | ID của bài kiểm tra     |

**Response:**
```json
{
  "exercise": {
    "id": 1,
    "specialization_id": 1,
    "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
    "difficulty_level": "easy",
    "duration": 45,
    "created_by": null,
    "created_at": "2026-02-28T00:00:00"
  },
  "questions": [
    {
      "id": 1,
      "exercise_id": 1,
      "content": "Biên độ dao động điều hòa x = 5cos(2πt + π/3) cm là?",
      "image_url": null,
      "type": "single",
      "level": "easy",
      "point": 1.0,
      "correct_text": null,
      "explanation": "Biên độ A = 5 cm",
      "created_at": "2026-02-28T00:00:00",
      "options": [
        { "id": 1, "question_id": 1, "content": "3 cm", "is_correct": false },
        { "id": 2, "question_id": 1, "content": "5 cm", "is_correct": true },
        { "id": 3, "question_id": 1, "content": "2π cm", "is_correct": false },
        { "id": 4, "question_id": 1, "content": "π/3 cm", "is_correct": false }
      ]
    }
  ]
}
```

> **Lưu ý:** `duration` tính bằng phút. Frontend nên ẩn `is_correct` và `explanation` khi học sinh đang làm bài.

---

## Content - Exam Submission & History

### POST /api/content/exam/submit

**Nộp bài kiểm tra, tự động chấm điểm trắc nghiệm. Câu essay lưu lại chờ giáo viên chấm (tự động nếu có `correct_text`).**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token | POST | `/api/content/exam/submit` |

**Request Body:**
```json
{
  "exercise_id": 1,
  "answers": [
    {
      "question_id": 1,
      "selected_option_ids": [2],
      "text_answer": null
    },
    {
      "question_id": 2,
      "selected_option_ids": [6],
      "text_answer": null
    },
    {
      "question_id": 3,
      "selected_option_ids": [],
      "text_answer": "Đáp án tự luận của học sinh"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| exercise_id | int | Yes | ID bài kiểm tra |
| answers | array | Yes | Danh sách câu trả lời |
| answers[].question_id | int | Yes | ID câu hỏi |
| answers[].selected_option_ids | int[] | No | Danh sách ID đáp án đã chọn (trắc nghiệm) |
| answers[].text_answer | string | No | Câu trả lời tự luận (essay) |

**Response (200):**
```json
{
  "attempt_id": 1,
  "total_score": 8.5,
  "total_questions": 10,
  "correct_count": 8,
  "total_points": 10.0,
  "earned_points": 8.5
}
```

> **Scoring Logic:**
> - **Single choice**: Đúng nếu chọn đúng 1 đáp án correct
> - **Multi choice**: Đúng nếu chọn đúng TẤT CẢ đáp án correct (không thừa, không thiếu)
> - **Essay**: Tự động chấm nếu có `correct_text` (so sánh không phân biệt hoa thường), nếu không điểm = 0 chờ giáo viên chấm
> - **Điểm tổng**: `(earned_points / total_points) * 10`

---

### GET /api/content/exam/history

**Lấy lịch sử tất cả các lần làm bài của user hiện tại, sắp xếp theo thời gian mới nhất.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token | GET | `/api/content/exam/history` |

**Response (200):**
```json
{
  "attempts": [
    {
      "id": 1,
      "account_id": 5,
      "exercise_id": 1,
      "total_score": 8.5,
      "started_at": "2026-03-05T10:00:00",
      "finished_at": "2026-03-05T10:30:00",
      "created_at": "2026-03-05T10:30:00",
      "exercise": {
        "id": 1,
        "specialization_id": 1,
        "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
        "difficulty_level": "easy",
        "duration": 45,
        "created_by": null,
        "created_at": "2026-02-28T00:00:00"
      }
    }
  ]
}
```

---

### GET /api/content/exam/history/exercise/{exercise_id}

**Lấy lịch sử các lần làm bài của user cho 1 bài kiểm tra cụ thể.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token | GET | `/api/content/exam/history/exercise/{exercise_id}` |

| Parameter   | Type | Required | Description             |
|-------------|------|----------|-------------------------|
| exercise_id | int  | Yes      | ID của bài kiểm tra     |

**Response (200):**
```json
{
  "attempts": [
    {
      "id": 1,
      "account_id": 5,
      "exercise_id": 1,
      "total_score": 8.5,
      "started_at": "2026-03-05T10:00:00",
      "finished_at": "2026-03-05T10:30:00",
      "created_at": "2026-03-05T10:30:00",
      "exercise": {
        "id": 1,
        "specialization_id": 1,
        "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
        "difficulty_level": "easy",
        "duration": 45,
        "created_by": null,
        "created_at": "2026-02-28T00:00:00"
      }
    }
  ]
}
```

---

### GET /api/content/exam/attempts/{attempt_id}

**Lấy chi tiết đầy đủ 1 lần làm bài: thông tin bài kiểm tra, câu hỏi, câu trả lời học sinh, điểm từng câu. Chỉ user tạo attempt mới được xem.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token | GET | `/api/content/exam/attempts/{attempt_id}` |

| Parameter  | Type | Required | Description          |
|------------|------|----------|----------------------|
| attempt_id | int  | Yes      | ID lần làm bài       |

**Response (200):**
```json
{
  "attempt": {
    "id": 1,
    "account_id": 5,
    "exercise_id": 1,
    "total_score": 7.5,
    "started_at": "2026-03-05T10:00:00",
    "finished_at": "2026-03-05T10:30:00",
    "created_at": "2026-03-05T10:30:00"
  },
  "exercise": {
    "id": 1,
    "specialization_id": 1,
    "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
    "difficulty_level": "easy",
    "duration": 45,
    "created_by": null,
    "created_at": "2026-02-28T00:00:00"
  },
  "responses": [
    {
      "id": 1,
      "attempt_id": 1,
      "question_id": 1,
      "text_answer": null,
      "teacher_comment": null,
      "score_earned": 1.0,
      "selected_choices": [
        { "id": 1, "response_id": 1, "selected_option_id": 2 }
      ],
      "question": {
        "id": 1,
        "exercise_id": 1,
        "content": "Biên độ dao động điều hòa x = 5cos(2πt + π/3) cm là?",
        "image_url": null,
        "type": "single",
        "level": "easy",
        "point": 1.0,
        "correct_text": null,
        "explanation": "Biên độ A = 5 cm",
        "created_at": "2026-02-28T00:00:00",
        "options": [
          { "id": 1, "question_id": 1, "content": "3 cm", "is_correct": false },
          { "id": 2, "question_id": 1, "content": "5 cm", "is_correct": true },
          { "id": 3, "question_id": 1, "content": "2π cm", "is_correct": false },
          { "id": 4, "question_id": 1, "content": "π/3 cm", "is_correct": false }
        ]
      }
    }
  ],
  "total_questions": 2,
  "correct_count": 1,
  "total_points": 3.0,
  "earned_points": 1.0
}
```

| Field | Type | Description |
|-------|------|-------------|
| attempt | object | Thông tin lần làm bài |
| exercise | object | Thông tin bài kiểm tra |
| responses | array | Chi tiết từng câu trả lời |
| responses[].selected_choices | array | Đáp án đã chọn (trắc nghiệm) |
| responses[].question | object | Câu hỏi + đáp án đúng |
| responses[].score_earned | float | Điểm đạt được cho câu này |
| total_questions | int | Tổng số câu hỏi |
| correct_count | int | Số câu đúng |
| total_points | float | Tổng điểm tối đa |
| earned_points | float | Tổng điểm đạt được |

> **Lưu ý:** Trả 403 nếu attempt không thuộc user hiện tại. Trả 404 nếu attempt không tồn tại.

---

## Content - Questions

### GET /api/content/exercises/{exercise_id}/questions

**Lấy danh sách câu hỏi theo bài kiểm tra (không kèm đáp án).**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/exercises/{exercise_id}/questions` |

| Parameter   | Type | Required | Description             |
|-------------|------|----------|-------------------------|
| exercise_id | int  | Yes      | ID của bài kiểm tra     |

**Response:**
```json
{
  "questions": [
    {
      "id": 1,
      "exercise_id": 1,
      "content": "Biên độ dao động điều hòa x = 5cos(2πt + π/3) cm là?",
      "image_url": null,
      "type": "single",
      "level": "easy",
      "point": 1.0,
      "correct_text": null,
      "explanation": "Biên độ A = 5 cm",
      "created_at": "2026-02-28T00:00:00"
    }
  ]
}
```

---

### GET /api/content/exercises/{exercise_id}/questions-with-options

**Lấy danh sách câu hỏi kèm đáp án theo bài kiểm tra.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/exercises/{exercise_id}/questions-with-options` |

| Parameter   | Type | Required | Description             |
|-------------|------|----------|-------------------------|
| exercise_id | int  | Yes      | ID của bài kiểm tra     |

**Response:**
```json
{
  "questions": [
    {
      "id": 1,
      "exercise_id": 1,
      "content": "Biên độ dao động điều hòa x = 5cos(2πt + π/3) cm là?",
      "image_url": null,
      "type": "single",
      "level": "easy",
      "point": 1.0,
      "correct_text": null,
      "explanation": "Biên độ A = 5 cm",
      "created_at": "2026-02-28T00:00:00",
      "options": [
        { "id": 1, "question_id": 1, "content": "3 cm", "is_correct": false },
        { "id": 2, "question_id": 1, "content": "5 cm", "is_correct": true },
        { "id": 3, "question_id": 1, "content": "2π cm", "is_correct": false },
        { "id": 4, "question_id": 1, "content": "π/3 cm", "is_correct": false }
      ]
    }
  ]
}
```

---

### GET /api/content/questions/{question_id}

**Lấy thông tin câu hỏi theo ID.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/questions/{question_id}` |

| Parameter   | Type | Required | Description         |
|-------------|------|----------|---------------------|
| question_id | int  | Yes      | ID của câu hỏi      |

**Response:**
```json
{
  "id": 1,
  "exercise_id": 1,
  "content": "Biên độ dao động điều hòa x = 5cos(2πt + π/3) cm là?",
  "image_url": null,
  "type": "single",
  "level": "easy",
  "point": 1.0,
  "correct_text": null,
  "explanation": "Biên độ A = 5 cm",
  "created_at": "2026-02-28T00:00:00"
}
```

---

### GET /api/content/questions/{question_id}/options

**Lấy danh sách đáp án của câu hỏi.**

| Auth | Method | Endpoint |
|------|--------|----------|
| PUBLIC | GET | `/api/content/questions/{question_id}/options` |

| Parameter   | Type | Required | Description         |
|-------------|------|----------|---------------------|
| question_id | int  | Yes      | ID của câu hỏi      |

**Response:**
```json
{
  "success": true,
  "data": [
    { "id": 1, "question_id": 1, "content": "3 cm", "is_correct": false },
    { "id": 2, "question_id": 1, "content": "5 cm", "is_correct": true },
    { "id": 3, "question_id": 1, "content": "2π cm", "is_correct": false },
    { "id": 4, "question_id": 1, "content": "π/3 cm", "is_correct": false }
  ]
}
```

---

## Admin - Dashboard

> **Tất cả API admin yêu cầu Bearer Token với role = `admin`. Trả 403 nếu không phải admin.**

### GET /api/admin/dashboard

**Thống kê tổng quan cho dashboard admin.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | GET | `/api/admin/dashboard` |

**Response (200):**
```json
{
  "total_users": 150,
  "total_students": 130,
  "total_teachers": 15,
  "total_admins": 5,
  "active_users": 140,
  "inactive_users": 10,
  "total_grades": 3,
  "total_topics": 25,
  "total_specializations": 80,
  "total_exercises": 200,
  "total_questions": 3000,
  "total_exam_attempts": 5000
}
```

---

### GET /api/admin/stats/exercises

**Thống kê theo bài kiểm tra: số lượt thi, điểm TB, cao nhất, thấp nhất.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | GET | `/api/admin/stats/exercises` |

**Response (200):**
```json
[
  {
    "exercise_id": 1,
    "exercise_name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
    "total_attempts": 120,
    "avg_score": 7.25,
    "highest_score": 10.0,
    "lowest_score": 2.0
  }
]
```

---

### GET /api/admin/stats/users

**Thống kê theo user: số lượt thi, điểm TB (top active users).**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | GET | `/api/admin/stats/users` |

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | int | No | Số lượng user trả về (default: 20, max: 100) |

**Response (200):**
```json
[
  {
    "user_id": 5,
    "email": "student@example.com",
    "full_name": "Nguyễn Văn A",
    "total_attempts": 45,
    "avg_score": 7.8
  }
]
```

---

## Admin - User Management

### GET /api/admin/users

**Lấy danh sách người dùng (phân trang, lọc, tìm kiếm).**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | GET | `/api/admin/users` |

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | int | No | Trang (default: 1) |
| page_size | int | No | Số item/trang (default: 20, max: 100) |
| role | string | No | Lọc theo role: `admin`, `student`, `teacher` |
| is_active | bool | No | Lọc theo trạng thái |
| search | string | No | Tìm theo email hoặc tên |

**Response (200):**
```json
{
  "users": [
    {
      "id": 1,
      "email": "admin@example.com",
      "full_name": "Admin",
      "role": "admin",
      "phone_number": null,
      "avatar_url": null,
      "address": null,
      "email_verified": true,
      "subscription_type": "free",
      "subscription_start": null,
      "subscription_end": null,
      "is_active": true,
      "created_at": "2026-01-01T00:00:00",
      "updated_at": "2026-03-10T00:00:00"
    }
  ],
  "total": 150,
  "page": 1,
  "page_size": 20
}
```

---

### GET /api/admin/users/{user_id}

**Xem chi tiết 1 user.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | GET | `/api/admin/users/{user_id}` |

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | int | Yes | ID người dùng |

**Response (200):** Giống 1 object trong danh sách users ở trên.

---

### PUT /api/admin/users/{user_id}

**Cập nhật thông tin user (role, trạng thái, subscription).**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | PUT | `/api/admin/users/{user_id}` |

**Request Body:**
```json
{
  "full_name": "Nguyễn Văn B",
  "role": "teacher",
  "is_active": true,
  "subscription_type": "pro"
}
```

> Tất cả field đều optional, chỉ gửi field cần thay đổi.

---

### PATCH /api/admin/users/{user_id}/deactivate

**Khóa tài khoản user.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | PATCH | `/api/admin/users/{user_id}/deactivate` |

---

### PATCH /api/admin/users/{user_id}/activate

**Mở khóa tài khoản user.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | PATCH | `/api/admin/users/{user_id}/activate` |

---

## Admin - Grade Management

### POST /api/admin/grades

**Tạo lớp học mới.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | POST | `/api/admin/grades` |

**Request Body:**
```json
{
  "name": "Lớp 10",
  "description": "Vật lý lớp 10"
}
```

---

### PUT /api/admin/grades/{grade_id}

**Cập nhật lớp học.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | PUT | `/api/admin/grades/{grade_id}` |

**Request Body:**
```json
{
  "name": "Lớp 10 - Cập nhật",
  "description": "Mô tả mới"
}
```

---

### DELETE /api/admin/grades/{grade_id}

**Xóa lớp học (cascade xóa topics, specializations, exercises, questions).**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | DELETE | `/api/admin/grades/{grade_id}` |

**Response (200):**
```json
{ "message": "Grade deleted successfully" }
```

---

## Admin - Topic Management

### POST /api/admin/topics

**Tạo chương học mới.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | POST | `/api/admin/topics` |

**Request Body:**
```json
{
  "grade_id": 1,
  "name": "Dao động cơ",
  "description": "Chương 1: Dao động cơ"
}
```

---

### PUT /api/admin/topics/{topic_id}

**Cập nhật chương học.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | PUT | `/api/admin/topics/{topic_id}` |

**Request Body:**
```json
{
  "grade_id": 1,
  "name": "Dao động cơ - Cập nhật",
  "description": "Mô tả mới"
}
```

---

### DELETE /api/admin/topics/{topic_id}

**Xóa chương học.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | DELETE | `/api/admin/topics/{topic_id}` |

**Response (200):**
```json
{ "message": "Topic deleted successfully" }
```

---

## Admin - Specialization Management

### POST /api/admin/specializations

**Tạo chuyên đề mới.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | POST | `/api/admin/specializations` |

**Request Body:**
```json
{
  "topic_id": 1,
  "name": "Dao động điều hòa",
  "description": "Lý thuyết + bài tập dao động điều hòa",
  "order_index": 1
}
```

---

### PUT /api/admin/specializations/{specialization_id}

**Cập nhật chuyên đề.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | PUT | `/api/admin/specializations/{specialization_id}` |

---

### DELETE /api/admin/specializations/{specialization_id}

**Xóa chuyên đề.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | DELETE | `/api/admin/specializations/{specialization_id}` |

**Response (200):**
```json
{ "message": "Specialization deleted successfully" }
```

---

## Admin - Exercise Management

### POST /api/admin/exercises

**Tạo bài kiểm tra mới.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | POST | `/api/admin/exercises` |

**Request Body:**
```json
{
  "specialization_id": 1,
  "name": "Bài kiểm tra: Dao động điều hòa - Cơ bản",
  "difficulty_level": "easy",
  "duration": 45
}
```

---

### PUT /api/admin/exercises/{exercise_id}

**Cập nhật bài kiểm tra.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | PUT | `/api/admin/exercises/{exercise_id}` |

---

### DELETE /api/admin/exercises/{exercise_id}

**Xóa bài kiểm tra.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | DELETE | `/api/admin/exercises/{exercise_id}` |

**Response (200):**
```json
{ "message": "Exercise deleted successfully" }
```

---

## Admin - Question Management

### POST /api/admin/questions

**Tạo câu hỏi mới (kèm đáp án nếu là trắc nghiệm).**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | POST | `/api/admin/questions` |

**Request Body (trắc nghiệm):**
```json
{
  "exercise_id": 1,
  "content": "Biên độ dao động điều hòa x = 5cos(2πt + π/3) cm là?",
  "image_url": "https://example.com/images/question1.png",
  "type": "single",
  "level": "easy",
  "point": 1.0,
  "explanation": "Biên độ A = 5 cm",
  "options": [
    { "content": "3 cm", "is_correct": false },
    { "content": "5 cm", "is_correct": true },
    { "content": "2π cm", "is_correct": false },
    { "content": "π/3 cm", "is_correct": false }
  ]
}
```

**Request Body (tự luận):**
```json
{
  "exercise_id": 1,
  "content": "Giải thích sự bảo toàn năng lượng trong dao động điều hòa.",
  "image_url": null,
  "type": "essay",
  "level": "hard",
  "point": 2.0,
  "correct_text": "Năng lượng được bảo toàn",
  "explanation": "Giải thích chi tiết..."
}
```

**Response (200):** Trả về câu hỏi + đáp án (QuestionWithOptions).

---

### PUT /api/admin/questions/{question_id}

**Cập nhật câu hỏi. Gửi `options` sẽ thay thế toàn bộ đáp án cũ.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | PUT | `/api/admin/questions/{question_id}` |

**Request Body:**
```json
{
  "content": "Câu hỏi cập nhật?",
  "point": 2.0,
  "options": [
    { "content": "Đáp án A", "is_correct": false },
    { "content": "Đáp án B", "is_correct": true }
  ]
}
```

> Tất cả field đều optional. Chỉ gửi field cần thay đổi.

---

### DELETE /api/admin/questions/{question_id}

**Xóa câu hỏi.**

| Auth | Method | Endpoint |
|------|--------|----------|
| Bearer Token (Admin) | DELETE | `/api/admin/questions/{question_id}` |

**Response (200):**
```json
{ "message": "Question deleted successfully" }
```

---

## Error Codes

| Error Code | Description |
|------------|-------------|
| `BAD_REQUEST` | Invalid request format |
| `UNAUTHORIZED` | Authentication failed |
| `FORBIDDEN` | Access denied |
| `NOT_FOUND` | Resource not found |
| `CONFLICT` | Resource conflict |
| `202` | Invalid data type or JSON |
| `221` | Default role not found |
| `227` | User not found |
| `233` | Email not verified |
| `234` | Refresh token expired |
| `238` | Email does not exist |
| `239` | Password is incorrect |
| `242` | OTP is expired |
| `243` | Required fields missing |
| `248` | Refresh token revoked |
| `249` | User is blocked |
| `255` | Email already exists |
| `602` | Invalid OTP / OTP attempts exceeded |

---

## Database Schema

### Tables
| Table | Description |
|-------|-------------|
| **accounts** | Tài khoản người dùng (email, password, role, subscription, tokens) |
| **grades** | Lớp học (Lớp 6 → 12) |
| **topics** | Chương học, liên kết với grades |
| **specializations** | Chuyên đề / Bài học, liên kết với topics |
| **exercises** | Bài kiểm tra, liên kết với specializations |
| **questions** | Câu hỏi, liên kết với exercises |
| **question_options** | Đáp án trắc nghiệm, liên kết với questions |
| **exam_attempts** | Lần làm bài của học sinh |
| **student_responses** | Câu trả lời của học sinh |
| **student_response_choices** | Đáp án đã chọn (trắc nghiệm) |

### Hierarchy
```
grades → topics → specializations → exercises → questions → question_options
                                              ↘ exam_attempts → student_responses → student_response_choices
```
