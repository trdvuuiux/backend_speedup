from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import datetime
from app.models.models import (
    Grade, Topic, Specialization, Exercise, Question, QuestionOption,
    ExamAttempt, StudentResponse, StudentResponseChoice
)


# ========================================================
# Grade CRUD
# ========================================================

def get_all_grades(db: Session):
    """Get all grades"""
    return db.query(Grade).all()


def get_grade_by_id(db: Session, grade_id: int):
    """Get grade by ID"""
    return db.query(Grade).filter(Grade.id == grade_id).first()


# ========================================================
# Topic CRUD
# ========================================================

def get_topics_by_grade(db: Session, grade_id: int):
    """Get all topics by grade ID"""
    return db.query(Topic).filter(Topic.grade_id == grade_id).all()


def get_topic_by_id(db: Session, topic_id: int):
    """Get topic by ID"""
    return db.query(Topic).filter(Topic.id == topic_id).first()


def get_all_topics(db: Session):
    """Get all topics"""
    return db.query(Topic).all()


# ========================================================
# Specialization CRUD
# ========================================================

def get_specializations_by_topic(db: Session, topic_id: int):
    """Get all specializations by topic ID"""
    return db.query(Specialization).filter(Specialization.topic_id == topic_id).order_by(Specialization.order_index).all()


def get_specialization_by_id(db: Session, specialization_id: int):
    """Get specialization by ID"""
    return db.query(Specialization).filter(Specialization.id == specialization_id).first()


def get_all_specializations(db: Session):
    """Get all specializations"""
    return db.query(Specialization).order_by(Specialization.order_index).all()


# ========================================================
# Exercise CRUD
# ========================================================

def get_exercises_by_specialization(db: Session, specialization_id: int):
    """Get all exercises by specialization ID"""
    return db.query(Exercise).filter(Exercise.specialization_id == specialization_id).all()


def get_exercise_by_id(db: Session, exercise_id: int):
    """Get exercise by ID"""
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()


def get_all_exercises(db: Session):
    """Get all exercises"""
    return db.query(Exercise).all()


def get_exercises_by_difficulty(db: Session, specialization_id: int, difficulty: str):
    """Get exercises by difficulty level"""
    return db.query(Exercise).filter(
        Exercise.specialization_id == specialization_id,
        Exercise.difficulty_level == difficulty
    ).all()


# ========================================================
# Question CRUD
# ========================================================

def get_questions_by_exercise(db: Session, exercise_id: int):
    """Get all questions by exercise ID"""
    return db.query(Question).filter(Question.exercise_id == exercise_id).all()


def get_questions_with_options_by_exercise(db: Session, exercise_id: int):
    """Get all questions with their options by exercise ID (eager load)"""
    return (
        db.query(Question)
        .options(joinedload(Question.options))
        .filter(Question.exercise_id == exercise_id)
        .all()
    )


def get_question_by_id(db: Session, question_id: int):
    """Get question by ID"""
    return db.query(Question).filter(Question.id == question_id).first()


def get_all_questions(db: Session):
    """Get all questions"""
    return db.query(Question).all()


# ========================================================
# QuestionOption CRUD
# ========================================================

def get_options_by_question(db: Session, question_id: int):
    """Get all options by question ID"""
    return db.query(QuestionOption).filter(QuestionOption.question_id == question_id).all()


def get_option_by_id(db: Session, option_id: int):
    """Get option by ID"""
    return db.query(QuestionOption).filter(QuestionOption.id == option_id).first()


# ========================================================
# ExamAttempt CRUD
# ========================================================

def submit_exam(db: Session, account_id: int, exercise_id: int, answers: list, started_at: datetime = None) -> dict:
    """
    Submit an exam: auto-grade single/multi choice questions, save all responses.
    Returns attempt with grading summary.
    """
    # Create exam attempt
    attempt = ExamAttempt(
        account_id=account_id,
        exercise_id=exercise_id,
        total_score=0,
        started_at=started_at or datetime.utcnow(),
        finished_at=datetime.utcnow()
    )
    db.add(attempt)
    db.flush()  # Get attempt.id

    total_questions = 0
    correct_count = 0
    total_points = 0.0
    earned_points = 0.0

    for answer in answers:
        question_id = answer.question_id
        selected_option_ids = answer.selected_option_ids
        text_answer = answer.text_answer

        # Get question info
        question = (
            db.query(Question)
            .options(joinedload(Question.options))
            .filter(Question.id == question_id)
            .first()
        )
        if not question:
            continue

        total_questions += 1
        total_points += question.point

        score_earned = 0.0

        if question.type in ('single', 'multi'):
            # Get correct option IDs
            correct_option_ids = {opt.id for opt in question.options if opt.is_correct}
            selected_set = set(selected_option_ids)

            # Check if answer is correct
            if selected_set == correct_option_ids and len(selected_set) > 0:
                score_earned = question.point
                correct_count += 1

        elif question.type == 'essay':
            # Essay: check if text matches correct_text (exact match for auto-grade)
            if question.correct_text and text_answer:
                if text_answer.strip().lower() == question.correct_text.strip().lower():
                    score_earned = question.point
                    correct_count += 1
            # Otherwise score_earned = 0, teacher can grade later

        earned_points += score_earned

        # Create student response
        response = StudentResponse(
            attempt_id=attempt.id,
            question_id=question_id,
            text_answer=text_answer,
            score_earned=score_earned
        )
        db.add(response)
        db.flush()

        # Save selected choices for single/multi
        for option_id in selected_option_ids:
            choice = StudentResponseChoice(
                response_id=response.id,
                selected_option_id=option_id
            )
            db.add(choice)

    # Update total score (percentage)
    attempt.total_score = round((earned_points / total_points * 10) if total_points > 0 else 0, 2)
    db.commit()
    db.refresh(attempt)

    return {
        "attempt": attempt,
        "total_questions": total_questions,
        "correct_count": correct_count,
        "total_points": total_points,
        "earned_points": earned_points
    }


def get_attempts_by_account(db: Session, account_id: int):
    """Get all exam attempts by account ID, newest first"""
    return (
        db.query(ExamAttempt)
        .options(joinedload(ExamAttempt.exercise))
        .filter(ExamAttempt.account_id == account_id)
        .order_by(ExamAttempt.created_at.desc())
        .all()
    )


def get_attempts_by_account_and_exercise(db: Session, account_id: int, exercise_id: int):
    """Get exam attempts by account ID and exercise ID"""
    return (
        db.query(ExamAttempt)
        .options(joinedload(ExamAttempt.exercise))
        .filter(
            ExamAttempt.account_id == account_id,
            ExamAttempt.exercise_id == exercise_id
        )
        .order_by(ExamAttempt.created_at.desc())
        .all()
    )


def get_attempt_by_id(db: Session, attempt_id: int):
    """Get exam attempt by ID"""
    return db.query(ExamAttempt).filter(ExamAttempt.id == attempt_id).first()


def get_attempt_detail(db: Session, attempt_id: int):
    """Get full attempt detail with responses, choices, and questions"""
    attempt = (
        db.query(ExamAttempt)
        .options(
            joinedload(ExamAttempt.exercise),
            joinedload(ExamAttempt.student_responses)
            .joinedload(StudentResponse.selected_choices),
            joinedload(ExamAttempt.student_responses)
            .joinedload(StudentResponse.question)
            .joinedload(Question.options),
        )
        .filter(ExamAttempt.id == attempt_id)
        .first()
    )
    return attempt
