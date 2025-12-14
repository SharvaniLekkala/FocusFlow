from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class FocusSession(Base):
    __tablename__ = "focus_sessions"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, index=True)
    duration = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
from sqlalchemy import Column, Integer, Date, ForeignKey
from datetime import date

class DailyProductivity(Base):
    __tablename__ = "daily_productivity"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Date, default=date.today)
    total_minutes = Column(Integer, default=0)
    session_count = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("users.id"))

