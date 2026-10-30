# PocketSmart AI

PocketSmart AI is a GenAI-powered budget and recommendation assistant.

The system supports:

- Home Interior Planning
- Party Budget Planning
- Jewelry Recommendations
- User Registration
- User Login
- JWT Authentication
- Recommendation History
- Gemini AI
- Optional Jewelry Outfit Image
- Responsive Web Interface
- FastAPI REST APIs
- SQLite Database

---

# Technologies

Backend:

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT
- bcrypt

Frontend:

- HTML
- CSS
- JavaScript
- Jinja2

AI:

- Google Gemini

---

# Project Structure

```text
PocketSmartAI/
│
├── run.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── uploads/
│
└── app/
    ├── main.py
    ├── config.py
    ├── database.py
    ├── models.py
    ├── auth.py
    ├── dependencies.py
    ├── schemas.py
    │
    ├── routers/
    │   ├── auth.py
    │   ├── planners.py
    │   └── pages.py
    │
    ├── services/
    │   ├── gemini_service.py
    │   └── recommendation_service.py
    │
    ├── templates/
    │
    └── static/