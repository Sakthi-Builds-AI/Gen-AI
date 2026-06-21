"""
routers/dashboard.py
----------------------
Powers the Executive Dashboard: the 8 KPI cards plus the data feeds for
the monthly trend and department-wise charts that the Streamlit frontend
renders with Plotly.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from database import get_db
from auth import get_current_user
import models
import schemas

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=schemas.DashboardSummary)
def summary(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    today = date.today()

    total_employees = db.query(models.Employee).filter(
        models.Employee.status == "Active"
    ).count()

    on_leave_today = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.status == "Approved",
        models.LeaveRequest.start_date <= today,
        models.LeaveRequest.end_date >= today,
    ).count()

    pending_requests = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.status == "Pending"
    ).count()

    approved_leaves = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.status == "Approved"
    ).count()

    rejected_leaves = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.status == "Rejected"
    ).count()

    upcoming_holidays = db.query(models.Holiday).filter(
        models.Holiday.holiday_date >= today
    ).count()

    # Utilization: approved leave-days taken so far this year vs. total
    # allocated balance pool (annual+sick+casual at creation, 36/head by default)
    year_start = date(today.year, 1, 1)
    approved_this_year = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.status == "Approved",
        models.LeaveRequest.start_date >= year_start,
    ).all()
    days_taken = sum((r.end_date - r.start_date).days + 1 for r in approved_this_year)
    allocated_pool = total_employees * 36  # 18+10+8 default allocation per employee
    utilization = round((days_taken / allocated_pool) * 100, 1) if allocated_pool else 0.0

    return schemas.DashboardSummary(
        total_employees=total_employees,
        present_today=max(total_employees - on_leave_today, 0),
        on_leave_today=on_leave_today,
        pending_requests=pending_requests,
        approved_leaves=approved_leaves,
        rejected_leaves=rejected_leaves,
        upcoming_holidays=upcoming_holidays,
        leave_utilization_pct=utilization,
    )


@router.get("/monthly-trend")
def monthly_trend(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    """Approved leave count grouped by month (current year) -- feeds the trend chart."""
    rows = db.query(
        func.strftime("%m", models.LeaveRequest.start_date).label("month"),
        func.count(models.LeaveRequest.leave_id).label("count"),
    ).filter(
        models.LeaveRequest.status == "Approved",
        func.strftime("%Y", models.LeaveRequest.start_date) == str(date.today().year),
    ).group_by("month").order_by("month").all()
    return [{"month": r.month, "count": r.count} for r in rows]


@router.get("/department-breakdown")
def department_breakdown(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    """Approved leave-days grouped by department -- feeds the department bar chart."""
    rows = db.query(models.LeaveRequest, models.Employee.department).join(
        models.Employee, models.LeaveRequest.employee_id == models.Employee.employee_id
    ).filter(models.LeaveRequest.status == "Approved").all()

    totals = {}
    for leave, dept in rows:
        days = (leave.end_date - leave.start_date).days + 1
        totals[dept] = totals.get(dept, 0) + days
    return [{"department": d, "days": days} for d, days in totals.items()]


@router.get("/leave-type-breakdown")
def leave_type_breakdown(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    """Count of approved requests grouped by leave type -- feeds the donut chart."""
    rows = db.query(
        models.LeaveRequest.leave_type, func.count(models.LeaveRequest.leave_id)
    ).filter(models.LeaveRequest.status == "Approved").group_by(
        models.LeaveRequest.leave_type
    ).all()
    return [{"leave_type": t, "count": c} for t, c in rows]
