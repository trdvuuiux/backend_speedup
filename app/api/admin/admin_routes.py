from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import decode_token
from app.crud.auth_crud import get_user_by_id
from app.crud import admin_crud, content_crud
from app.models.models import Account
from app.schemas.admin_schema import (
    # Grade
    GradeCreateRequest, GradeUpdateRequest,
    # Topic
    TopicCreateRequest, TopicUpdateRequest,
    # Specialization
    SpecializationCreateRequest, SpecializationUpdateRequest,
    # Exercise
    ExerciseCreateRequest, ExerciseUpdateRequest,
    # Question
    QuestionCreateRequest, QuestionUpdateRequest,
    # User
    UserUpdateRequest, UserResponse, UserListResponse,
    # Stats
    DashboardStatsResponse, ExerciseStatsResponse, UserExamStatsResponse,
    MessageResponse,
)
from app.schemas.content_schema import (
    GradeResponse, TopicResponse, SpecializationResponse,
    ExerciseResponse, QuestionResponse, QuestionWithOptions,
)

router = APIRouter(prefix="/api/admin", tags=["Admin"])
security = HTTPBearer()


# ========================================================
# Admin Dependency — kiểm tra role admin
# ========================================================

async def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token")
    try:
        user_id = int(payload.get("sub"))
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ========================================================
# GRADE MANAGEMENT
# ========================================================

@router.post("/grades", response_model=GradeResponse)
async def create_grade(
    request: GradeCreateRequest,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Tạo lớp học mới"""
    grade = admin_crud.create_grade(db, name=request.name, description=request.description)
    return GradeResponse.model_validate(grade)


@router.put("/grades/{grade_id}", response_model=GradeResponse)
async def update_grade(
    grade_id: int,
    request: GradeUpdateRequest,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Cập nhật lớp học"""
    grade = admin_crud.update_grade(db, grade_id, name=request.name, description=request.description)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return GradeResponse.model_validate(grade)


@router.delete("/grades/{grade_id}", response_model=MessageResponse)
async def delete_grade(
    grade_id: int,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Xóa lớp học (cascade xóa topics, specializations, exercises, questions)"""
    success = admin_crud.delete_grade(db, grade_id)
    if not success:
        raise HTTPException(status_code=404, detail="Grade not found")
    return MessageResponse(message="Grade deleted successfully")


# ========================================================
# TOPIC MANAGEMENT
# ========================================================

@router.post("/topics", response_model=TopicResponse)
async def create_topic(
    request: TopicCreateRequest,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Tạo chương học mới"""
    # Check grade exists
    grade = content_crud.get_grade_by_id(db, request.grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    topic = admin_crud.create_topic(db, grade_id=request.grade_id, name=request.name, description=request.description)
    return TopicResponse.model_validate(topic)


@router.put("/topics/{topic_id}", response_model=TopicResponse)
async def update_topic(
    topic_id: int,
    request: TopicUpdateRequest,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Cập nhật chương học"""
    if request.grade_id:
        grade = content_crud.get_grade_by_id(db, request.grade_id)
        if not grade:
            raise HTTPException(status_code=404, detail="Grade not found")
    topic = admin_crud.update_topic(db, topic_id, grade_id=request.grade_id, name=request.name, description=request.description)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return TopicResponse.model_validate(topic)


@router.delete("/topics/{topic_id}", response_model=MessageResponse)
async def delete_topic(
    topic_id: int,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Xóa chương học"""
    success = admin_crud.delete_topic(db, topic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Topic not found")
    return MessageResponse(message="Topic deleted successfully")


# ========================================================
# SPECIALIZATION MANAGEMENT
# ========================================================

@router.post("/specializations", response_model=SpecializationResponse)
async def create_specialization(
    request: SpecializationCreateRequest,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Tạo chuyên đề mới"""
    topic = content_crud.get_topic_by_id(db, request.topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    spec = admin_crud.create_specialization(
        db, topic_id=request.topic_id, name=request.name,
        description=request.description, order_index=request.order_index,
        created_by=admin.id
    )
    return SpecializationResponse.model_validate(spec)


@router.put("/specializations/{specialization_id}", response_model=SpecializationResponse)
async def update_specialization(
    specialization_id: int,
    request: SpecializationUpdateRequest,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Cập nhật chuyên đề"""
    if request.topic_id:
        topic = content_crud.get_topic_by_id(db, request.topic_id)
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
    spec = admin_crud.update_specialization(
        db, specialization_id,
        topic_id=request.topic_id, name=request.name,
        description=request.description, order_index=request.order_index
    )
    if not spec:
        raise HTTPException(status_code=404, detail="Specialization not found")
    return SpecializationResponse.model_validate(spec)


@router.delete("/specializations/{specialization_id}", response_model=MessageResponse)
async def delete_specialization(
    specialization_id: int,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Xóa chuyên đề"""
    success = admin_crud.delete_specialization(db, specialization_id)
    if not success:
        raise HTTPException(status_code=404, detail="Specialization not found")
    return MessageResponse(message="Specialization deleted successfully")


# ========================================================
# EXERCISE MANAGEMENT
# ========================================================

@router.post("/exercises", response_model=ExerciseResponse)
async def create_exercise(
    request: ExerciseCreateRequest,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Tạo bài kiểm tra mới"""
    spec = content_crud.get_specialization_by_id(db, request.specialization_id)
    if not spec:
        raise HTTPException(status_code=404, detail="Specialization not found")
    exercise = admin_crud.create_exercise(
        db, specialization_id=request.specialization_id, name=request.name,
        difficulty_level=request.difficulty_level, time_limit=request.time_limit,
        created_by=admin.id
    )
    return ExerciseResponse.model_validate(exercise)


@router.put("/exercises/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: int,
    request: ExerciseUpdateRequest,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Cập nhật bài kiểm tra"""
    if request.specialization_id:
        spec = content_crud.get_specialization_by_id(db, request.specialization_id)
        if not spec:
            raise HTTPException(status_code=404, detail="Specialization not found")
    exercise = admin_crud.update_exercise(
        db, exercise_id,
        specialization_id=request.specialization_id, name=request.name,
        difficulty_level=request.difficulty_level, time_limit=request.time_limit
    )
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return ExerciseResponse.model_validate(exercise)


@router.delete("/exercises/{exercise_id}", response_model=MessageResponse)
async def delete_exercise(
    exercise_id: int,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Xóa bài kiểm tra"""
    success = admin_crud.delete_exercise(db, exercise_id)
    if not success:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return MessageResponse(message="Exercise deleted successfully")


# ========================================================
# QUESTION MANAGEMENT
# ========================================================

@router.post("/questions", response_model=QuestionWithOptions)
async def create_question(
    request: QuestionCreateRequest,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Tạo câu hỏi mới (kèm đáp án nếu là trắc nghiệm)"""
    exercise = content_crud.get_exercise_by_id(db, request.exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    question = admin_crud.create_question(
        db, exercise_id=request.exercise_id, content=request.content,
        type=request.type, level=request.level, point=request.point,
        correct_text=request.correct_text, explanation=request.explanation,
        image_url=request.image_url, options=request.options
    )
    # Reload with options
    question = content_crud.get_question_by_id(db, question.id)
    db.refresh(question)
    return QuestionWithOptions.model_validate(question)


@router.put("/questions/{question_id}", response_model=QuestionWithOptions)
async def update_question(
    question_id: int,
    request: QuestionUpdateRequest,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Cập nhật câu hỏi (gửi options = thay thế toàn bộ đáp án cũ)"""
    if request.exercise_id:
        exercise = content_crud.get_exercise_by_id(db, request.exercise_id)
        if not exercise:
            raise HTTPException(status_code=404, detail="Exercise not found")
    question = admin_crud.update_question(
        db, question_id, options=request.options,
        exercise_id=request.exercise_id, content=request.content,
        type=request.type, level=request.level, point=request.point,
        correct_text=request.correct_text, explanation=request.explanation
    )
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.refresh(question)
    return QuestionWithOptions.model_validate(question)


@router.delete("/questions/{question_id}", response_model=MessageResponse)
async def delete_question(
    question_id: int,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Xóa câu hỏi"""
    success = admin_crud.delete_question(db, question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return MessageResponse(message="Question deleted successfully")


# ========================================================
# USER MANAGEMENT
# ========================================================

@router.get("/users", response_model=UserListResponse)
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Lấy danh sách người dùng (phân trang, lọc role, tìm kiếm)"""
    users, total = admin_crud.get_all_users(db, page=page, page_size=page_size, role=role, is_active=is_active, search=search)
    return UserListResponse(
        users=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Xem chi tiết 1 user"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    request: UserUpdateRequest,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Cập nhật thông tin user (role, is_active, subscription...)"""
    user = admin_crud.update_user_by_admin(
        db, user_id,
        full_name=request.full_name, role=request.role,
        is_active=request.is_active, subscription_type=request.subscription_type
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)


@router.patch("/users/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: int,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Khóa tài khoản user"""
    user = admin_crud.deactivate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)


@router.patch("/users/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: int,
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Mở khóa tài khoản user"""
    user = admin_crud.activate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)


# ========================================================
# DASHBOARD & STATISTICS
# ========================================================

@router.get("/dashboard", response_model=DashboardStatsResponse)
async def get_dashboard(
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Thống kê tổng quan cho dashboard"""
    stats = admin_crud.get_dashboard_stats(db)
    return DashboardStatsResponse(**stats)


@router.get("/stats/exercises", response_model=list[ExerciseStatsResponse])
async def get_exercise_stats(
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Thống kê theo bài kiểm tra: số lượt thi, điểm TB, cao nhất, thấp nhất"""
    stats = admin_crud.get_exercise_stats(db)
    return [ExerciseStatsResponse(**s) for s in stats]


@router.get("/stats/users", response_model=list[UserExamStatsResponse])
async def get_user_exam_stats(
    limit: int = Query(20, ge=1, le=100),
    admin: Account = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Thống kê theo user: số lượt thi, điểm TB (top active users)"""
    stats = admin_crud.get_user_exam_stats(db, limit=limit)
    return [UserExamStatsResponse(**s) for s in stats]
