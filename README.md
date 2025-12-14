# FocusFlow  
A Full-Stack Productivity Tracking & Analytics Platform

FocusFlow is a full-stack web application designed to help users track focus sessions, manage daily productivity cycles, and analyze work trends over time.  
The project emphasizes **clean backend design, secure authentication, and time-based analytics**, making it a strong example of real-world full-stack engineering.

---

##  Key Features

-  Secure user authentication using JWT
-  Create and manage focus sessions (task + duration)
-  Clear daily sessions to start each day fresh
-  Automatic aggregation of productivity data
-  Weekly and monthly productivity summaries
-  User-specific data isolation and authorization

---

##  Why FocusFlow?

Many productivity tools focus only on logging tasks.  
FocusFlow goes a step further by **modeling time-based behavior**, allowing users to:

- Track how much time they focus each day
- Observe weekly and monthly productivity trends
- Reset daily sessions without losing historical data
- Gain meaningful insights from aggregated data

This project prioritizes **engineering correctness and product thinking** over superficial features.

---

##  Tech Stack

### Frontend
- React (Vite)
- JavaScript
- Axios

### Backend
- FastAPI
- SQLAlchemy ORM
- SQLite
- JWT Authentication


---

##  Authentication Flow

1. User registers with email and password
2. User logs in to receive a JWT access token
3. Token is required for all protected routes
4. Backend validates token and isolates user data

This ensures secure, multi-user access to the platform.

---

##  Productivity Analytics

FocusFlow generates insights using **backend aggregation logic**, not external AI services.

### Available Insights:
- Total focus time
- Average focus per day
- Weekly productivity summary
- Monthly productivity summary
- Session count trends

These insights are calculated from raw session data and stored daily records.

---

Sharvani Lekkala



