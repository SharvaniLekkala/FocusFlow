from sqlalchemy.orm import Session
from .models import User
from .auth import hash_password, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str):
    user = User(email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

from .models import FocusSession

def create_focus_session(db, task_name, duration, user_id):
    session = FocusSession(
        task_name=task_name,
        duration=duration,
        user_id=user_id
    )
    db.add(session)

    daily = get_or_create_today_productivity(db, user_id)
    daily.total_minutes += duration
    daily.session_count += 1

    db.commit()
    db.refresh(session)
    return session


def get_user_sessions(db, user_id):
    return db.query(FocusSession).filter(
        FocusSession.user_id == user_id
    ).all()

from collections import Counter

def generate_insights(sessions):
    if not sessions:
        return {
            "total_minutes": 0,
            "top_task": None,
            "average_session": 0,
            "summary": "No focus sessions yet. Start tracking your work!"
        }

    total_minutes = sum(s.duration for s in sessions)
    avg_session = total_minutes // len(sessions)

    task_counts = Counter(s.task_name for s in sessions)
    top_task = task_counts.most_common(1)[0][0]

    summary = (
        f"You are most focused on {top_task} tasks. "
        f"Your average focus session is {avg_session} minutes."
    )

    return {
        "total_minutes": total_minutes,
        "top_task": top_task,
        "average_session": avg_session,
        "summary": summary
    }
from datetime import date
from .models import DailyProductivity

def get_or_create_today_productivity(db, user_id):
    today = date.today()
    record = db.query(DailyProductivity).filter(
        DailyProductivity.user_id == user_id,
        DailyProductivity.day == today
    ).first()

    if not record:
        record = DailyProductivity(
            user_id=user_id,
            day=today,
            total_minutes=0,
            session_count=0
        )
        db.add(record)
        db.commit()
        db.refresh(record)

    return record
from datetime import date
from .models import FocusSession

def delete_today_sessions(db, user_id):
    today = date.today()

    sessions = db.query(FocusSession).filter(
        FocusSession.user_id == user_id,
        FocusSession.created_at >= today
    ).all()

    for s in sessions:
        db.delete(s)

    db.query(DailyProductivity).filter(
        DailyProductivity.user_id == user_id,
        DailyProductivity.day == today
    ).delete()

    db.commit()
from datetime import date, timedelta

def get_summary(db, user_id, range_type: str):
    today = date.today()

    if range_type == "week":
        start = today - timedelta(days=7)
    elif range_type == "month":
        start = today - timedelta(days=30)
    else:
        return None

    records = db.query(DailyProductivity).filter(
        DailyProductivity.user_id == user_id,
        DailyProductivity.day >= start
    ).all()

    if not records:
        return {
            "total_minutes": 0,
            "average_daily_minutes": 0,
            "days_tracked": 0
        }

    total = sum(r.total_minutes for r in records)
    days = len(records)

    return {
        "total_minutes": total,
        "average_daily_minutes": total // days,
        "days_tracked": days
    }
