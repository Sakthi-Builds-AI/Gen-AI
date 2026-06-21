"""
main.py
-------
FastAPI application entrypoint.

Run with:  cd backend && uvicorn main:app --reload --port 8000
Docs at:   http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import auth_routes, employees, departments, holidays, leaves, dashboard, reports, notifications

# Create all tables if they don't exist yet (seed_data.py populates sample rows)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Leave Management Portal API",
    description="Smart Leave Planning. Seamless Workforce Management.",
    version="1.0.0",
)

# Streamlit runs on a different port, so it needs CORS clearance to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(holidays.router)
app.include_router(leaves.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
app.include_router(notifications.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "Leave Management Portal API"}
