from sqlalchemy import Column, Integer, String, Enum, Text, DateTime, Boolean, Double, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Account(Base):
    """Tài khoản người dùng"""
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=True)
    role = Column(Enum('admin', 'student', 'teacher'), default='student')

    # Thông tin bổ sung
    phone_number = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    address = Column(String(255), nullable=True)

    # Xác thực & Token
    otp = Column(String(10), nullable=True)
    created_otp = Column(DateTime, nullable=True)
    otp_attempts = Column(Integer, default=0)  # Max 5 attempts
    email_verified = Column(Boolean, default=False)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)

    # Subscription
    subscription_type = Column(Enum('free', 'plus', 'pro', 'vip', 'max'), default='free')
    subscription_start = Column(DateTime, nullable=True)
    subscription_end = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    created_specializations = relationship("Specialization", back_populates="creator")
    created_exercises = relationship("Exercise", back_populates="creator")
    exam_attempts = relationship("ExamAttempt", back_populates="account")


class Grade(Base):
    """Lớp học (10, 11, 12)"""
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)

    # Relationships
    topics = relationship("Topic", back_populates="grade")


class Topic(Base):
    """Chương học"""
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    grade_id = Column(Integer, ForeignKey("grades.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    grade = relationship("Grade", back_populates="topics")
    specializations = relationship("Specialization", back_populates="topic")


class Specialization(Base):
    """Chuyên đề"""
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey("accounts.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    topic = relationship("Topic", back_populates="specializations")
    creator = relationship("Account", back_populates="created_specializations")
    exercises = relationship("Exercise", back_populates="specialization")


class Exercise(Base):
    """Bài tập / Bài kiểm tra"""
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    specialization_id = Column(Integer, ForeignKey("specializations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    difficulty_level = Column(Enum('easy', 'medium', 'hard', 'expert'), default='medium')
    time_limit = Column(Integer, default=45)
    created_by = Column(Integer, ForeignKey("accounts.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    specialization = relationship("Specialization", back_populates="exercises")
    creator = relationship("Account", back_populates="created_exercises")
    questions = relationship("Question", back_populates="exercise")
    exam_attempts = relationship("ExamAttempt", back_populates="exercise")


class Question(Base):
    """Câu hỏi"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)
    type = Column(Enum('single', 'multi', 'essay'), nullable=False)
    level = Column(Enum('easy', 'medium', 'hard'), default='medium')
    point = Column(Double, default=1.0)
    correct_text = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    exercise = relationship("Exercise", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan")
    student_responses = relationship("StudentResponse", back_populates="question")


class QuestionOption(Base):
    """Đáp án cho câu trắc nghiệm"""
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    # Relationships
    question = relationship("Question", back_populates="options")
    student_response_choices = relationship("StudentResponseChoice", back_populates="selected_option")


class ExamAttempt(Base):
    """Lần làm bài"""
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    total_score = Column(Double, default=0)
    started_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    account = relationship("Account", back_populates="exam_attempts")
    exercise = relationship("Exercise", back_populates="exam_attempts")
    student_responses = relationship("StudentResponse", back_populates="attempt", cascade="all, delete-orphan")


class StudentResponse(Base):
    """Chi tiết câu trả lời"""
    __tablename__ = "student_responses"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("exam_attempts.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    text_answer = Column(Text, nullable=True)
    teacher_comment = Column(Text, nullable=True)
    score_earned = Column(Double, default=0)

    # Relationships
    attempt = relationship("ExamAttempt", back_populates="student_responses")
    question = relationship("Question", back_populates="student_responses")
    selected_choices = relationship("StudentResponseChoice", back_populates="response", cascade="all, delete-orphan")


class StudentResponseChoice(Base):
    """Đáp án trắc nghiệm đã chọn"""
    __tablename__ = "student_response_choices"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("student_responses.id", ondelete="CASCADE"), nullable=False)
    selected_option_id = Column(Integer, ForeignKey("question_options.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    response = relationship("StudentResponse", back_populates="selected_choices")
    selected_option = relationship("QuestionOption", back_populates="student_response_choices")
