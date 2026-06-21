"""
routers/leaves.py
-------------------
Core leave workflow: apply, list (mine / my team / everyone), and
manager approve/reject/clarify decisions. Also exposes a simple
team-availability check (who else is approved-off in a date range).

Deduction policy (documented assumption): only Casual Leave, Sick Leave
and Earned Leave draw down a numeric balance, and only once a manager
APPROVES the request (not at apply time). Maternity, Paternity, WFH,
Compensatory Off and Half Day Leave are tracked for visibility/approval
but don't deduct from the three numeric balance buckets in this MVP.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date
from typing import List, Optional

from database import get_db
from auth import get_current_user, require_role
import models
import schemas

router = APIRouter(prefix="/api/leaves", tags=["Leaves"])

# Which leave types draw down which LeaveBalance column
BALANCE_FIELD_BY_TYPE = {
    "Casual Leave": "casual_leave",
    "Sick Leave": "sick_leave",
    "Earned Leave": "annual_leave",
}


def _days_requested(start_date: date, end_date: date) -> int:
    return (end_date - start_date).days + 1


def _notify(db: Session, username: str, message: str, leave_id: int = None):
    """Queues a Notification row. Silently no-ops if the recipient has no
    login (e.g. a manager field that isn't wired to a Users row)."""
    if not username:
        return
    db.add(models.Notification(
        recipient_username=username, message=message, leave_id=leave_id,
    ))


def _to_out(req: models.LeaveRequest) -> schemas.LeaveRequestOut:
    return schemas.LeaveRequestOut(
        leave_id=req.leave_id,
        employee_id=req.employee_id,
        employee_name=req.employee.employee_name if req.employee else None,
        department=req.employee.department if req.employee else None,
        leave_type=req.leave_type,
        start_date=req.start_date,
        end_date=req.end_date,
        days_requested=_days_requested(req.start_date, req.end_date),
        reason=req.reason,
        emergency_contact=req.emergency_contact,
        status=req.status,
        manager_comments=req.manager_comments,
        applied_on=req.applied_on,
    )


@router.post("", response_model=schemas.LeaveRequestOut)
def apply_leave(
    payload: schemas.LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if payload.end_date < payload.start_date:
        raise HTTPException(status_code=400, detail="End date cannot be before start date")

    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == payload.employee_id
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Overlap / conflict detection against the employee's own existing requests
    overlap = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.employee_id == payload.employee_id,
        models.LeaveRequest.status.in_(["Pending", "Approved"]),
        models.LeaveRequest.start_date <= payload.end_date,
        models.LeaveRequest.end_date >= payload.start_date,
    ).first()
    if overlap:
        raise HTTPException(
            status_code=400,
            detail=f"This overlaps an existing {overlap.status.lower()} request "
                   f"({overlap.start_date} to {overlap.end_date})",
        )

    leave = models.LeaveRequest(**payload.model_dump(), status="Pending")
    db.add(leave)
    db.flush()  # assigns leave.leave_id before we reference it below

    # Notify the employee's manager, if their manager has a linked login
    if employee.manager:
        manager_user = db.query(models.User).filter(
            models.User.employee_id == employee.manager
        ).first()
        if manager_user:
            _notify(
                db, manager_user.username,
                f"{employee.employee_name} applied for {leave.leave_type} "
                f"({leave.start_date} to {leave.end_date}) — awaiting your approval.",
                leave.leave_id,
            )

    db.commit()
    db.refresh(leave)
    return _to_out(leave)


@router.get("/my", response_model=List[schemas.LeaveRequestOut])
def my_leaves(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not current_user.employee_id:
        raise HTTPException(status_code=400, detail="This account has no linked employee record")
    rows = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.employee_id == current_user.employee_id
    ).order_by(models.LeaveRequest.applied_on.desc()).all()
    return [_to_out(r) for r in rows]


@router.get("/team", response_model=List[schemas.LeaveRequestOut])
def team_leaves(
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("Manager", "HR Admin", "Super Admin")),
):
    """Requests from people who report to the current manager."""
    query = db.query(models.LeaveRequest).join(models.Employee).filter(
        models.Employee.manager == current_user.employee_id
    )
    if status_filter:
        query = query.filter(models.LeaveRequest.status == status_filter)
    rows = query.order_by(models.LeaveRequest.applied_on.desc()).all()
    return [_to_out(r) for r in rows]


@router.get("", response_model=List[schemas.LeaveRequestOut])
def all_leaves(
    status_filter: Optional[str] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db),
    _user=Depends(require_role("HR Admin", "Super Admin")),
):
    query = db.query(models.LeaveRequest).join(models.Employee)
    if status_filter:
        query = query.filter(models.LeaveRequest.status == status_filter)
    if department:
        query = query.filter(models.Employee.department == department)
    rows = query.order_by(models.LeaveRequest.applied_on.desc()).all()
    return [_to_out(r) for r in rows]


@router.post("/{leave_id}/decision", response_model=schemas.LeaveRequestOut)
def decide_leave(
    leave_id: int,
    payload: schemas.LeaveRequestDecision,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("Manager", "HR Admin", "Super Admin")),
):
    leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.leave_id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")

    valid_statuses = {"Approved", "Rejected", "Clarification Requested"}
    if payload.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of {valid_statuses}")

    if payload.status == "Approved":
        balance_field = BALANCE_FIELD_BY_TYPE.get(leave.leave_type)
        if balance_field:
            bal = db.query(models.LeaveBalance).filter(
                models.LeaveBalance.employee_id == leave.employee_id
            ).first()
            days = _days_requested(leave.start_date, leave.end_date)
            current_value = getattr(bal, balance_field) if bal else 0
            if bal and current_value < days:
                raise HTTPException(
                    status_code=400,
                    detail=f"Employee only has {current_value} days of {leave.leave_type} left "
                           f"(requested {days})",
                )
            if bal:
                setattr(bal, balance_field, current_value - days)

    leave.status = payload.status
    leave.manager_comments = payload.manager_comments

    # Notify the employee whose request this was, if they have a login
    employee_user = db.query(models.User).filter(
        models.User.employee_id == leave.employee_id
    ).first()
    if employee_user:
        verdict = {
            "Approved": "approved ✅",
            "Rejected": "rejected ❌",
            "Clarification Requested": "sent back for clarification 💬",
        }.get(payload.status, payload.status.lower())
        _notify(
            db, employee_user.username,
            f"Your {leave.leave_type} request ({leave.start_date} to {leave.end_date}) was {verdict}.",
            leave.leave_id,
        )

    db.commit()
    db.refresh(leave)
    return _to_out(leave)


@router.get("/team-availability")
def team_availability(
    start_date: date,
    end_date: date,
    department: Optional[str] = None,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    """Who is approved-off in a given window -- powers the Team Availability widget."""
    query = db.query(models.LeaveRequest).join(models.Employee).filter(
        models.LeaveRequest.status == "Approved",
        models.LeaveRequest.start_date <= end_date,
        models.LeaveRequest.end_date >= start_date,
    )
    if department:
        query = query.filter(models.Employee.department == department)
    rows = query.all()
    return [
        {
            "employee_id": r.employee_id,
            "employee_name": r.employee.employee_name,
            "department": r.employee.department,
            "leave_type": r.leave_type,
            "start_date": r.start_date,
            "end_date": r.end_date,
        }
        for r in rows
    ]
