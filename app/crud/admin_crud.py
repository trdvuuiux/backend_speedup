from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models.models import (
    Account, Role, Grade, Topic, Specialization, Exercise,
    Question, QuestionOption, ExamAttempt
)


# ========================================================
# Grade CRUD (Admin)
# ========================================================

def create_grade(db: Session, name: str, description: str = None):
    grade = Grade(name=name, description=description)
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade


def update_grade(db: Session, grade_id: int, **kwargs):
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        return None
    for key, value in kwargs.items():
        if value is not None:
            setattr(grade, key, value)
    db.commit()
    db.refresh(grade)
    return grade


def delete_grade(db: Session, grade_id: int):
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        return False
    db.delete(grade)
    db.commit()
    return True


# ========================================================
# Topic CRUD (Admin)
# ========================================================

def create_topic(db: Session, grade_id: int, name: str, description: str = None):
    topic = Topic(grade_id=grade_id, name=name, description=description)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


def update_topic(db: Session, topic_id: int, **kwargs):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        return None
    for key, value in kwargs.items():
        if value is not None:
            setattr(topic, key, value)
    db.commit()
    db.refresh(topic)
    return topic


def delete_topic(db: Session, topic_id: int):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        return False
    db.delete(topic)
    db.commit()
    return True


# ========================================================
# Specialization CRUD (Admin)
# ========================================================

def create_specialization(db: Session, topic_id: int, name: str, description: str = None, order_index: int = 0, created_by: int = None):
    spec = Specialization(
        topic_id=topic_id, name=name, description=description,
        order_index=order_index, created_by=created_by
    )
    db.add(spec)
    db.commit()
    db.refresh(spec)
    return spec


def update_specialization(db: Session, specialization_id: int, **kwargs):
    spec = db.query(Specialization).filter(Specialization.id == specialization_id).first()
    if not spec:
        return None
    for key, value in kwargs.items():
        if value is not None:
            setattr(spec, key, value)
    db.commit()
    db.refresh(spec)
    return spec


def delete_specialization(db: Session, specialization_id: int):
    spec = db.query(Specialization).filter(Specialization.id == specialization_id).first()
    if not spec:
        return False
    db.delete(spec)
    db.commit()
    return True


# ========================================================
# Exercise CRUD (Admin)
# ========================================================

def create_exercise(db: Session, specialization_id: int, name: str, difficulty_level: str = 'medium', duration: int = 45, created_by: int = None):
    exercise = Exercise(
        specialization_id=specialization_id, name=name,
        difficulty_level=difficulty_level, duration=duration,
        created_by=created_by
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def update_exercise(db: Session, exercise_id: int, **kwargs):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return None
    for key, value in kwargs.items():
        if value is not None:
            setattr(exercise, key, value)
    db.commit()
    db.refresh(exercise)
    return exercise


def delete_exercise(db: Session, exercise_id: int):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return False
    # Xóa các exam_attempts liên quan trước
    db.query(ExamAttempt).filter(ExamAttempt.exercise_id == exercise_id).delete()
    # Xóa các questions liên quan trước
    db.query(Question).filter(Question.exercise_id == exercise_id).delete()
    db.delete(exercise)
    db.commit()
    return True


# ========================================================
# Question CRUD (Admin) — tạo câu hỏi + đáp án cùng lúc
# ========================================================

def create_question(db: Session, exercise_id: int, content: str, type: str, level: str = 'medium', point: float = 1.0, correct_text: str = None, explanation: str = None, image_url: str = None, options: list = None):
    question = Question(
        exercise_id=exercise_id, content=content, image_url=image_url, type=type,
        level=level, point=point, correct_text=correct_text,
        explanation=explanation
    )
    db.add(question)
    db.flush()

    if options:
        for opt in options:
            option = QuestionOption(
                question_id=question.id,
                content=opt.content,
                is_correct=opt.is_correct
            )
            db.add(option)

    db.commit()
    db.refresh(question)
    return question


def update_question(db: Session, question_id: int, options: list = None, **kwargs):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return None

    for key, value in kwargs.items():
        if value is not None:
            setattr(question, key, value)

    # Nếu gửi options mới → xóa cũ, tạo mới
    if options is not None:
        db.query(QuestionOption).filter(QuestionOption.question_id == question_id).delete()
        for opt in options:
            option = QuestionOption(
                question_id=question_id,
                content=opt.content,
                is_correct=opt.is_correct
            )
            db.add(option)

    db.commit()
    db.refresh(question)
    return question


def delete_question(db: Session, question_id: int):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return False
    db.delete(question)
    db.commit()
    return True


# ========================================================
# User Management (Admin)
# ========================================================

def get_all_users(db: Session, page: int = 1, page_size: int = 20, role: str = None, is_active: bool = None, search: str = None):
    query = db.query(Account).options(joinedload(Account.role_rel)).join(Role, Account.role_id == Role.id)

    if role:
        query = query.filter(Role.name == role)
    if is_active is not None:
        query = query.filter(Account.is_active == is_active)
    if search:
        query = query.filter(
            (Account.email.ilike(f"%{search}%")) |
            (Account.full_name.ilike(f"%{search}%"))
        )

    total = query.count()
    users = query.order_by(Account.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return users, total


def update_user_by_admin(db: Session, user_id: int, **kwargs):
    user = db.query(Account).options(joinedload(Account.role_rel)).filter(Account.id == user_id).first()
    if not user:
        return None
    
    # Handle role separately — convert role name to role_id
    role_name = kwargs.pop('role', None)
    if role_name is not None:
        role = db.query(Role).filter(Role.name == role_name).first()
        if role:
            user.role_id = role.id
    
    for key, value in kwargs.items():
        if value is not None:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def deactivate_user(db: Session, user_id: int):
    user = db.query(Account).filter(Account.id == user_id).first()
    if not user:
        return None
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


def activate_user(db: Session, user_id: int):
    user = db.query(Account).filter(Account.id == user_id).first()
    if not user:
        return None
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user


# ========================================================
# Dashboard / Statistics (Admin)
# ========================================================

def get_dashboard_stats(db: Session):
    total_users = db.query(func.count(Account.id)).scalar()
    total_students = db.query(func.count(Account.id)).join(Role, Account.role_id == Role.id).filter(Role.name == 'student').scalar()
    total_teachers = db.query(func.count(Account.id)).join(Role, Account.role_id == Role.id).filter(Role.name == 'teacher').scalar()
    total_admins = db.query(func.count(Account.id)).join(Role, Account.role_id == Role.id).filter(Role.name == 'admin').scalar()
    active_users = db.query(func.count(Account.id)).filter(Account.is_active == True).scalar()
    inactive_users = db.query(func.count(Account.id)).filter(Account.is_active == False).scalar()
    total_grades = db.query(func.count(Grade.id)).scalar()
    total_topics = db.query(func.count(Topic.id)).scalar()
    total_specializations = db.query(func.count(Specialization.id)).scalar()
    total_exercises = db.query(func.count(Exercise.id)).scalar()
    total_questions = db.query(func.count(Question.id)).scalar()
    total_exam_attempts = db.query(func.count(ExamAttempt.id)).scalar()

    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_admins": total_admins,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "total_grades": total_grades,
        "total_topics": total_topics,
        "total_specializations": total_specializations,
        "total_exercises": total_exercises,
        "total_questions": total_questions,
        "total_exam_attempts": total_exam_attempts,
    }


def get_exercise_stats(db: Session):
    results = (
        db.query(
            Exercise.id,
            Exercise.name,
            func.count(ExamAttempt.id).label("total_attempts"),
            func.avg(ExamAttempt.total_score).label("avg_score"),
            func.max(ExamAttempt.total_score).label("highest_score"),
            func.min(ExamAttempt.total_score).label("lowest_score"),
        )
        .outerjoin(ExamAttempt, ExamAttempt.exercise_id == Exercise.id)
        .group_by(Exercise.id, Exercise.name)
        .order_by(func.count(ExamAttempt.id).desc())
        .all()
    )
    return [
        {
            "exercise_id": r.id,
            "exercise_name": r.name,
            "total_attempts": r.total_attempts,
            "avg_score": round(float(r.avg_score), 2) if r.avg_score else None,
            "highest_score": float(r.highest_score) if r.highest_score else None,
            "lowest_score": float(r.lowest_score) if r.lowest_score else None,
        }
        for r in results
    ]


def get_user_exam_stats(db: Session, limit: int = 20):
    results = (
        db.query(
            Account.id,
            Account.email,
            Account.full_name,
            func.count(ExamAttempt.id).label("total_attempts"),
            func.avg(ExamAttempt.total_score).label("avg_score"),
        )
        .outerjoin(ExamAttempt, ExamAttempt.account_id == Account.id)
        .group_by(Account.id, Account.email, Account.full_name)
        .order_by(func.count(ExamAttempt.id).desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "user_id": r.id,
            "email": r.email,
            "full_name": r.full_name,
            "total_attempts": r.total_attempts,
            "avg_score": round(float(r.avg_score), 2) if r.avg_score else None,
        }
        for r in results
    ]
