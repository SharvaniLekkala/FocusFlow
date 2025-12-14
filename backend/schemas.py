from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

from datetime import datetime

class FocusSessionCreate(BaseModel):
    task_name: str
    duration: int

class FocusSessionResponse(BaseModel):
    id: int
    task_name: str
    duration: int
    created_at: datetime

    class Config:
        from_attributes = True

class InsightsResponse(BaseModel):
    total_minutes: int
    top_task: str | None
    average_session: int
    summary: str
class SummaryResponse(BaseModel):
    total_minutes: int
    average_daily_minutes: int
    days_tracked: int
