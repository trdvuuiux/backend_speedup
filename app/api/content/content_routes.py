from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import decode_token
from app.crud.auth_crud import get_user_by_id
from app.models.models import Account
from app.schemas.content_schema import (
    GradeResponse,
    GradeListResponse,
    TopicResponse,
    TopicListResponse,
    SpecializationResponse,
    SpecializationListResponse,
    ExerciseResponse,
    ExerciseListResponse,
    QuestionResponse,
    QuestionListResponse,
    QuestionOptionResponse,
    QuestionWithOptions,
    QuestionWithOptionsListResponse,
    ExamDetailResponse,
    ExamSubmissionRequest,
    ExamSubmissionResultResponse,
    ExamAttemptResponse,
    ExamAttemptWithExercise,
    ExamAttemptListResponse,
    ExamAttemptDetailResponse,
    StudentResponseDetailResponse,
    StudentResponseChoiceResponse,
)
from app.crud import content_crud

router = APIRouter(prefix="/api/content", tags=["Content"])
security = HTTPBearer()


# Dependency to get current user
async def get_current_user(
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
    return user


# ========================================================
# GRADES
# ========================================================

@router.get("/grades", response_model=GradeListResponse)
async def get_grades(db: Session = Depends(get_db)):
    """
    Get all grades (Lớp 10, 11, 12)
    """
    grades = content_crud.get_all_grades(db)
    return GradeListResponse(grades=[GradeResponse.model_validate(g) for g in grades])


@router.get("/grades/{grade_id}", response_model=GradeResponse)
async def get_grade(grade_id: int, db: Session = Depends(get_db)):
    """
    Get grade by ID
    """
    grade = content_crud.get_grade_by_id(db, grade_id)
    if not grade:
        return {"success": False, "errorCode": "404", "errorMessage": "Grade not found", "data": None}
    return GradeResponse.model_validate(grade)


# ========================================================
# TOPICS
# ========================================================

@router.get("/grades/{grade_id}/topics", response_model=TopicListResponse)
async def get_topics_by_grade(grade_id: int, db: Session = Depends(get_db)):
    """
    Get all topics by grade ID
    """
    topics = content_crud.get_topics_by_grade(db, grade_id)
    return TopicListResponse(topics=[TopicResponse.model_validate(t) for t in topics])


@router.get("/topics", response_model=TopicListResponse)
async def get_all_topics(db: Session = Depends(get_db)):
    """
    Get all topics
    """
    topics = content_crud.get_all_topics(db)
    return TopicListResponse(topics=[TopicResponse.model_validate(t) for t in topics])


@router.get("/topics/{topic_id}", response_model=TopicResponse)
async def get_topic(topic_id: int, db: Session = Depends(get_db)):
    """
    Get topic by ID
    """
    topic = content_crud.get_topic_by_id(db, topic_id)
    if not topic:
        return {"success": False, "errorCode": "404", "errorMessage": "Topic not found", "data": None}
    return TopicResponse.model_validate(topic)


# ========================================================
# SPECIALIZATIONS
# ========================================================

@router.get("/topics/{topic_id}/specializations", response_model=SpecializationListResponse)
async def get_specializations_by_topic(topic_id: int, db: Session = Depends(get_db)):
    """
    Get all specializations by topic ID
    """
    specializations = content_crud.get_specializations_by_topic(db, topic_id)
    return SpecializationListResponse(specializations=[SpecializationResponse.model_validate(s) for s in specializations])


@router.get("/specializations", response_model=SpecializationListResponse)
async def get_all_specializations(db: Session = Depends(get_db)):
    """
    Get all specializations
    """
    specializations = content_crud.get_all_specializations(db)
    return SpecializationListResponse(specializations=[SpecializationResponse.model_validate(s) for s in specializations])


@router.get("/specializations/{specialization_id}", response_model=SpecializationResponse)
async def get_specialization(specialization_id: int, db: Session = Depends(get_db)):
    """
    Get specialization by ID
    """
    specialization = content_crud.get_specialization_by_id(db, specialization_id)
    if not specialization:
        return {"success": False, "errorCode": "404", "errorMessage": "Specialization not found", "data": None}
    return SpecializationResponse.model_validate(specialization)


# ========================================================
# EXERCISES
# ========================================================

@router.get("/specializations/{specialization_id}/exercises", response_model=ExerciseListResponse)
async def get_exercises_by_specialization(specialization_id: int, db: Session = Depends(get_db)):
    """
    Get all exercises by specialization ID
    """
    exercises = content_crud.get_exercises_by_specialization(db, specialization_id)
    return ExerciseListResponse(exercises=[ExerciseResponse.model_validate(e) for e in exercises])


@router.get("/specializations/{specialization_id}/exercises/difficulty/{difficulty}", response_model=ExerciseListResponse)
async def get_exercises_by_difficulty(specialization_id: int, difficulty: str, db: Session = Depends(get_db)):
    """
    Get exercises by difficulty level
    """
    exercises = content_crud.get_exercises_by_difficulty(db, specialization_id, difficulty)
    return ExerciseListResponse(exercises=[ExerciseResponse.model_validate(e) for e in exercises])


@router.get("/exercises", response_model=ExerciseListResponse)
async def get_all_exercises(db: Session = Depends(get_db)):
    """
    Get all exercises
    """
    exercises = content_crud.get_all_exercises(db)
    return ExerciseListResponse(exercises=[ExerciseResponse.model_validate(e) for e in exercises])


@router.get("/exercises/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """
    Get exercise by ID
    """
    exercise = content_crud.get_exercise_by_id(db, exercise_id)
    if not exercise:
        return {"success": False, "errorCode": "404", "errorMessage": "Exercise not found", "data": None}
    return ExerciseResponse.model_validate(exercise)


# ========================================================
# EXAM (Bài thi - Exercise + Questions + Options)
# ========================================================

@router.get("/exercises/{exercise_id}/exam", response_model=ExamDetailResponse)
async def get_exam_detail(exercise_id: int, db: Session = Depends(get_db)):
    """
    Get exercise info with all questions and their options (for taking an exam)
    """
    exercise = content_crud.get_exercise_by_id(db, exercise_id)
    if not exercise:
        return {"success": False, "errorCode": "404", "errorMessage": "Exercise not found", "data": None}
    questions = content_crud.get_questions_with_options_by_exercise(db, exercise_id)
    return ExamDetailResponse(
        exercise=ExerciseResponse.model_validate(exercise),
        questions=[QuestionWithOptions.model_validate(q) for q in questions]
    )


# ========================================================
# QUESTIONS
# ========================================================

@router.get("/exercises/{exercise_id}/questions", response_model=QuestionListResponse)
async def get_questions_by_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """
    Get all questions by exercise ID
    """
    questions = content_crud.get_questions_by_exercise(db, exercise_id)
    return QuestionListResponse(questions=[QuestionResponse.model_validate(q) for q in questions])


@router.get("/exercises/{exercise_id}/questions-with-options", response_model=QuestionWithOptionsListResponse)
async def get_questions_with_options(exercise_id: int, db: Session = Depends(get_db)):
    """
    Get all questions with their answer options by exercise ID
    """
    questions = content_crud.get_questions_with_options_by_exercise(db, exercise_id)
    return QuestionWithOptionsListResponse(
        questions=[QuestionWithOptions.model_validate(q) for q in questions]
    )


@router.get("/questions/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    """
    Get question by ID
    """
    question = content_crud.get_question_by_id(db, question_id)
    if not question:
        return {"success": False, "errorCode": "404", "errorMessage": "Question not found", "data": None}
    return QuestionResponse.model_validate(question)


@router.get("/questions/{question_id}/options")
async def get_question_options(question_id: int, db: Session = Depends(get_db)):
    """
    Get all options for a question
    """
    options = content_crud.get_options_by_question(db, question_id)
    return {"success": True, "data": [QuestionOptionResponse.model_validate(o) for o in options]}


# ========================================================
# EXAM SUBMISSION (Nộp bài & Chấm điểm)
# ========================================================

@router.post("/exam/submit", response_model=ExamSubmissionResultResponse)
async def submit_exam(
    request: ExamSubmissionRequest,
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit an exam: save student answers and auto-grade.
    - Single/Multi choice: auto-graded immediately
    - Essay: saved for teacher to grade later (auto-grade if correct_text exists)
    """
    # Check exercise exists
    exercise = content_crud.get_exercise_by_id(db, request.exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    result = content_crud.submit_exam(
        db=db,
        account_id=current_user.id,
        exercise_id=request.exercise_id,
        answers=request.answers,
        started_at=request.started_at
    )

    return ExamSubmissionResultResponse(
        attempt_id=result["attempt"].id,
        total_score=result["attempt"].total_score,
        total_questions=result["total_questions"],
        correct_count=result["correct_count"],
        total_points=result["total_points"],
        earned_points=result["earned_points"]
    )


# ========================================================
# EXAM HISTORY (Lịch sử làm bài)
# ========================================================

@router.get("/exam/history", response_model=ExamAttemptListResponse)
async def get_exam_history(
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all exam attempts for the current user (newest first)
    """
    attempts = content_crud.get_attempts_by_account(db, current_user.id)
    return ExamAttemptListResponse(
        attempts=[
            ExamAttemptWithExercise(
                **ExamAttemptResponse.model_validate(a).model_dump(),
                exercise=ExerciseResponse.model_validate(a.exercise)
            )
            for a in attempts
        ]
    )


@router.get("/exam/history/exercise/{exercise_id}", response_model=ExamAttemptListResponse)
async def get_exam_history_by_exercise(
    exercise_id: int,
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get exam attempts for a specific exercise (current user)
    """
    attempts = content_crud.get_attempts_by_account_and_exercise(db, current_user.id, exercise_id)
    return ExamAttemptListResponse(
        attempts=[
            ExamAttemptWithExercise(
                **ExamAttemptResponse.model_validate(a).model_dump(),
                exercise=ExerciseResponse.model_validate(a.exercise)
            )
            for a in attempts
        ]
    )


@router.get("/exam/attempts/{attempt_id}", response_model=ExamAttemptDetailResponse)
async def get_attempt_detail(
    attempt_id: int,
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get full detail of an exam attempt: exercise info, all questions, student answers, scores
    """
    attempt = content_crud.get_attempt_detail(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    # Only allow owner to view their attempt
    if attempt.account_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Build response detail
    responses_detail = []
    correct_count = 0
    total_points = 0.0
    earned_points = 0.0

    for resp in attempt.student_responses:
        question = resp.question
        total_points += question.point
        earned_points += resp.score_earned
        if resp.score_earned == question.point and question.point > 0:
            correct_count += 1

        responses_detail.append(
            StudentResponseDetailResponse(
                id=resp.id,
                attempt_id=resp.attempt_id,
                question_id=resp.question_id,
                text_answer=resp.text_answer,
                teacher_comment=resp.teacher_comment,
                score_earned=resp.score_earned,
                selected_choices=[
                    StudentResponseChoiceResponse.model_validate(c)
                    for c in resp.selected_choices
                ],
                question=QuestionWithOptions.model_validate(question)
            )
        )

    return ExamAttemptDetailResponse(
        attempt=ExamAttemptResponse.model_validate(attempt),
        exercise=ExerciseResponse.model_validate(attempt.exercise),
        responses=responses_detail,
        total_questions=len(attempt.student_responses),
        correct_count=correct_count,
        total_points=total_points,
        earned_points=earned_points
    )
