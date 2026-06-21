"""
routers/reports.py
---------------------
Reports & Analytics data feeds. Returns plain JSON; the Streamlit
frontend turns this into downloadable CSV/Excel files via pandas
(see frontend/reports_page.py). Keeping export-file-generation on the
frontend avoids the backend needing to manage temp files.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from auth import require_role
import models

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/leave-summary")
def leave_summary(
    department: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    _user=Depends(require_role("Manager", "HR Admin", "Super Admin")),
):
    query = db.query(models.LeaveRequest).join(models.Employee)
    if department:
        query = query.filter(models.Employee.department == department)
    if status_filter:
        query = query.filter(models.LeaveRequest.status == status_filter)
    rows = query.all()
    return [
        {
            "leave_id": r.leave_id,
            "employee_id": r.employee_id,
            "employee_name": r.employee.employee_name,
            "department": r.employee.department,
            "leave_type": r.leave_type,
            "start_date": str(r.start_date),
            "end_date": str(r.end_date),
            "days": (r.end_date - r.start_date).days + 1,
            "status": r.status,
            "applied_on": str(r.applied_on),
        }
        for r in rows
    ]


@router.get("/employee-directory")
def employee_directory(
    db: Session = Depends(get_db),
    _user=Depends(require_role("HR Admin", "Super Admin")),
):
    rows = db.query(models.Employee).all()
    return [
        {
            "employee_id": e.employee_id,
            "employee_name": e.employee_name,
            "email": e.email,
            "department": e.department,
            "manager": e.manager,
            "joining_date": str(e.joining_date),
            "status": e.status,
        }
        for e in rows
    ]


@router.get("/attendance-analysis")
def attendance_analysis(
    db: Session = Depends(get_db),
    _user=Depends(require_role("Manager", "HR Admin", "Super Admin")),
):
    """Per-employee count of approved leave days -- a simple attendance proxy."""
    employees = db.query(models.Employee).filter(models.Employee.status == "Active").all()
    result = []
    for e in employees:
        approved = [r for r in e.leave_requests if r.status == "Approved"]
        days_off = sum((r.end_date - r.start_date).days + 1 for r in approved)
        result.append({
            "employee_id": e.employee_id,
            "employee_name": e.employee_name,
            "department": e.department,
            "approved_requests": len(approved),
            "total_days_off": days_off,
        })
    return result
