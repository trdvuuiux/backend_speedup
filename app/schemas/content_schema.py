from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ========================================================
# Grade (Lớp học)
# ========================================================

class GradeBase(BaseModel):
    """Base Grade schema"""
    name: str
    description: Optional[str] = None


class GradeResponse(GradeBase):
    """Grade response schema"""
    id: int

    class Config:
        from_attributes = True


# ========================================================
# Topic (Chương học)
# ========================================================

class TopicBase(BaseModel):
    """Base Topic schema"""
    grade_id: int
    name: str
    description: Optional[str] = None


class TopicResponse(TopicBase):
    """Topic response schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TopicWithGrade(TopicResponse):
    """Topic with grade info"""
    grade: GradeResponse


# ========================================================
# Specialization (Chuyên đề)
# ========================================================

class SpecializationBase(BaseModel):
    """Base Specialization schema"""
    topic_id: int
    name: str
    description: Optional[str] = None
    order_index: int = 0


class SpecializationResponse(SpecializationBase):
    """Specialization response schema"""
    id: int
    created_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SpecializationWithTopic(SpecializationResponse):
    """Specialization with topic info"""
    topic: TopicResponse


# ========================================================
# Exercise (Bài tập)
# ========================================================

class ExerciseBase(BaseModel):
    """Base Exercise schema"""
    specialization_id: int
    name: str
    difficulty_level: str = 'medium'
    time_limit: int = 45


class ExerciseResponse(ExerciseBase):
    """Exercise response schema"""
    id: int
    created_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ExerciseWithSpecialization(ExerciseResponse):
    """Exercise with specialization info"""
    specialization: SpecializationResponse


# ========================================================
# Question (Câu hỏi)
# ========================================================

class QuestionBase(BaseModel):
    """Base Question schema"""
    exercise_id: int
    content: str
    image_url: Optional[str] = None
    type: str  # single, multi, essay
    level: str = 'medium'
    point: float = 1.0
    correct_text: Optional[str] = None
    explanation: Optional[str] = None


class QuestionResponse(QuestionBase):
    """Question response schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionWithOptions(QuestionResponse):
    """Question with options"""
    options: list["QuestionOptionResponse"] = []


# ========================================================
# QuestionOption (Đáp án)
# ========================================================

class QuestionOptionBase(BaseModel):
    """Base QuestionOption schema"""
    question_id: int
    content: str
    is_correct: bool = False


class QuestionOptionResponse(QuestionOptionBase):
    """QuestionOption response schema"""
    id: int

    class Config:
        from_attributes = True


# ========================================================
# List Response
# ========================================================

class GradeListResponse(BaseModel):
    """Grade list response"""
    grades: list[GradeResponse]


class TopicListResponse(BaseModel):
    """Topic list response"""
    topics: list[TopicResponse]


class SpecializationListResponse(BaseModel):
    """Specialization list response"""
    specializations: list[SpecializationResponse]


class ExerciseListResponse(BaseModel):
    """Exercise list response"""
    exercises: list[ExerciseResponse]


class QuestionListResponse(BaseModel):
    """Question list response"""
    questions: list[QuestionResponse]


class QuestionWithOptionsListResponse(BaseModel):
    """Question with options list response"""
    questions: list[QuestionWithOptions]


class ExamDetailResponse(BaseModel):
    """Exam detail: exercise info + all questions with options"""
    exercise: ExerciseResponse
    questions: list[QuestionWithOptions]


# ========================================================
# Exam Submission (Nộp bài)
# ========================================================

class AnswerSubmission(BaseModel):
    """Single answer submission for a question"""
    question_id: int
    selected_option_ids: list[int] = []      # For single/multi choice
    text_answer: Optional[str] = None         # For essay questions


class ExamSubmissionRequest(BaseModel):
    """Request to submit an exam"""
    exercise_id: int
    started_at: datetime          # Thời điểm bắt đầu làm bài (frontend gửi lên)
    answers: list[AnswerSubmission]


# ========================================================
# Exam Attempt Response (Kết quả bài thi)
# ========================================================

class StudentResponseChoiceResponse(BaseModel):
    """Student's selected option"""
    id: int
    response_id: int
    selected_option_id: int

    class Config:
        from_attributes = True


class StudentResponseResponse(BaseModel):
    """Student's response to a question"""
    id: int
    attempt_id: int
    question_id: int
    text_answer: Optional[str] = None
    teacher_comment: Optional[str] = None
    score_earned: float = 0

    class Config:
        from_attributes = True


class StudentResponseDetailResponse(StudentResponseResponse):
    """Student's response with selected choices and question info"""
    selected_choices: list[StudentResponseChoiceResponse] = []
    question: QuestionWithOptions


class ExamAttemptResponse(BaseModel):
    """Exam attempt summary"""
    id: int
    account_id: int
    exercise_id: int
    total_score: float
    started_at: datetime
    finished_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ExamAttemptWithExercise(ExamAttemptResponse):
    """Exam attempt with exercise info"""
    exercise: ExerciseResponse


class ExamAttemptDetailResponse(BaseModel):
    """Full exam attempt detail with all responses"""
    attempt: ExamAttemptResponse
    exercise: ExerciseResponse
    responses: list[StudentResponseDetailResponse]
    total_questions: int
    correct_count: int
    total_points: float
    earned_points: float


class ExamAttemptListResponse(BaseModel):
    """List of exam attempts"""
    attempts: list[ExamAttemptWithExercise]


class ExamSubmissionResultResponse(BaseModel):
    """Result returned after submitting an exam"""
    attempt_id: int
    total_score: float
    total_questions: int
    correct_count: int
    total_points: float
    earned_points: float
