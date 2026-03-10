from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ========================================================
# Admin - Grade Management
# ========================================================

class GradeCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None


class GradeUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None


# ========================================================
# Admin - Topic Management
# ========================================================

class TopicCreateRequest(BaseModel):
    grade_id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class TopicUpdateRequest(BaseModel):
    grade_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


# ========================================================
# Admin - Specialization Management
# ========================================================

class SpecializationCreateRequest(BaseModel):
    topic_id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    order_index: int = 0


class SpecializationUpdateRequest(BaseModel):
    topic_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    order_index: Optional[int] = None


# ========================================================
# Admin - Exercise Management
# ========================================================

class ExerciseCreateRequest(BaseModel):
    specialization_id: int
    name: str = Field(..., min_length=1, max_length=255)
    difficulty_level: str = 'medium'
    time_limit: int = 45


class ExerciseUpdateRequest(BaseModel):
    specialization_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    difficulty_level: Optional[str] = None
    time_limit: Optional[int] = None


# ========================================================
# Admin - Question Management
# ========================================================

class QuestionOptionCreateRequest(BaseModel):
    content: str = Field(..., min_length=1)
    is_correct: bool = False


class QuestionCreateRequest(BaseModel):
    exercise_id: int
    content: str = Field(..., min_length=1)
    image_url: Optional[str] = None
    type: str  # single, multi, essay
    level: str = 'medium'
    point: float = 1.0
    correct_text: Optional[str] = None
    explanation: Optional[str] = None
    options: list[QuestionOptionCreateRequest] = []


class QuestionOptionUpdateRequest(BaseModel):
    id: Optional[int] = None   # None = new option, có id = update
    content: str = Field(..., min_length=1)
    is_correct: bool = False


class QuestionUpdateRequest(BaseModel):
    exercise_id: Optional[int] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    type: Optional[str] = None
    level: Optional[str] = None
    point: Optional[float] = None
    correct_text: Optional[str] = None
    explanation: Optional[str] = None
    options: Optional[list[QuestionOptionUpdateRequest]] = None


# ========================================================
# Admin - User Management
# ========================================================

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None       # admin, student, teacher
    is_active: Optional[bool] = None
    subscription_type: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    role: str
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    address: Optional[str] = None
    email_verified: bool = False
    subscription_type: str = 'free'
    subscription_start: Optional[datetime] = None
    subscription_end: Optional[datetime] = None
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
    page: int
    page_size: int


# ========================================================
# Admin - Dashboard / Statistics
# ========================================================

class DashboardStatsResponse(BaseModel):
    total_users: int
    total_students: int
    total_teachers: int
    total_admins: int
    active_users: int
    inactive_users: int
    total_grades: int
    total_topics: int
    total_specializations: int
    total_exercises: int
    total_questions: int
    total_exam_attempts: int


class ExerciseStatsResponse(BaseModel):
    exercise_id: int
    exercise_name: str
    total_attempts: int
    avg_score: Optional[float] = None
    highest_score: Optional[float] = None
    lowest_score: Optional[float] = None


class UserExamStatsResponse(BaseModel):
    user_id: int
    email: str
    full_name: Optional[str] = None
    total_attempts: int
    avg_score: Optional[float] = None


class MessageResponse(BaseModel):
    message: str
