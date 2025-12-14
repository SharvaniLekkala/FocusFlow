from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas, crud, auth
from .database import SessionLocal, engine

print(">>> MAIN.PY LOADED <<<")

# Create tables
models.Base.metadata.create_all(bind=engine)
print(">>> DATABASE TABLES CREATED <<<")

app = FastAPI(title="FocusFlow API")

# -------------------- CORS (VERY IMPORTANT) --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------------------

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- AUTH ROUTES --------------------
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user.email, user.password)


@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
# ----------------------------------------------------


# -------------------- FOCUS SESSIONS --------------------
@app.post("/sessions", response_model=schemas.FocusSessionResponse)
def create_session(
    session: schemas.FocusSessionCreate,
    db: Session = Depends(get_db),
    email: str = Depends(auth.get_current_user_email),
):
    user = crud.get_user_by_email(db, email)
    return crud.create_focus_session(
        db, session.task_name, session.duration, user.id
    )


@app.get("/sessions", response_model=list[schemas.FocusSessionResponse])
def get_sessions(
    db: Session = Depends(get_db),
    email: str = Depends(auth.get_current_user_email),
):
    user = crud.get_user_by_email(db, email)
    return crud.get_user_sessions(db, user.id)
# -------------------------------------------------------


# -------------------- INSIGHTS --------------------
@app.get("/insights", response_model=schemas.InsightsResponse)
def get_insights(
    db: Session = Depends(get_db),
    email: str = Depends(auth.get_current_user_email),
):
    user = crud.get_user_by_email(db, email)
    sessions = crud.get_user_sessions(db, user.id)
    return crud.generate_insights(sessions)
# ------------------------------------------------
@app.delete("/sessions/today")
def clear_today_sessions(
    db: Session = Depends(get_db),
    email: str = Depends(auth.get_current_user_email)
):
    user = crud.get_user_by_email(db, email)
    crud.delete_today_sessions(db, user.id)
    return {"message": "Today's sessions cleared"}
@app.get("/summary/{range_type}", response_model=schemas.SummaryResponse)
def get_summary(
    range_type: str,
    db: Session = Depends(get_db),
    email: str = Depends(auth.get_current_user_email)
):
    user = crud.get_user_by_email(db, email)
    summary = crud.get_summary(db, user.id, range_type)

    if not summary:
        raise HTTPException(status_code=400, detail="Invalid range")

    return summary
