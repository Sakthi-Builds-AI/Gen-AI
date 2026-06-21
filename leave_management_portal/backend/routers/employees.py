"""
routers/employees.py
----------------------
Employee Management module (HR Admin module from the spec):
add, edit, deactivate, list, and search employees. Creating an employee
also seeds a default LeaveBalance row, and optionally a login (Users row)
if username/password are supplied.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from auth import get_current_user, require_role, hash_password
import models
import schemas

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.get("", response_model=List[schemas.EmployeeOut])
def list_employees(
    search: Optional[str] = None,
    department: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = db.query(models.Employee)
    if search:
        like = f"%{search}%"
        query = query.filter(
            (models.Employee.employee_name.ilike(like))
            | (models.Employee.employee_id.ilike(like))
            | (models.Employee.email.ilike(like))
        )
    if department:
        query = query.filter(models.Employee.department == department)
    if status_filter:
        query = query.filter(models.Employee.status == status_filter)
    return query.order_by(models.Employee.employee_name).all()


@router.get("/{employee_id}", response_model=schemas.EmployeeOut)
def get_employee(
    employee_id: str, db: Session = Depends(get_db), _user=Depends(get_current_user)
):
    emp = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.post("", response_model=schemas.EmployeeOut)
def create_employee(
    payload: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    _user=Depends(require_role("HR Admin", "Super Admin")),
):
    if db.query(models.Employee).filter(models.Employee.employee_id == payload.employee_id).first():
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    emp = models.Employee(
        employee_id=payload.employee_id,
        employee_name=payload.employee_name,
        email=payload.email,
        department=payload.department,
        manager=payload.manager,
        joining_date=payload.joining_date,
        status=payload.status,
    )
    db.add(emp)

    # Seed a default leave balance for the new hire
    db.add(models.LeaveBalance(employee_id=payload.employee_id))

    # Optionally create login credentials alongside the employee record
    if payload.username and payload.password:
        if db.query(models.User).filter(models.User.username == payload.username).first():
            raise HTTPException(status_code=400, detail="Username already taken")
        db.add(models.User(
            username=payload.username,
            password_hash=hash_password(payload.password),
            role=payload.role or "Employee",
            employee_id=payload.employee_id,
            full_name=payload.employee_name,
        ))

    db.commit()
    db.refresh(emp)
    return emp


@router.put("/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee(
    employee_id: str,
    payload: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_role("HR Admin", "Super Admin")),
):
    emp = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(emp, field, value)
    db.commit()
    db.refresh(emp)
    return emp


@router.post("/{employee_id}/deactivate", response_model=schemas.EmployeeOut)
def deactivate_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    _user=Depends(require_role("HR Admin", "Super Admin")),
):
    emp = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    emp.status = "Inactive"
    db.commit()
    db.refresh(emp)
    return emp


@router.get("/{employee_id}/balance", response_model=schemas.LeaveBalanceOut)
def get_balance(
    employee_id: str, db: Session = Depends(get_db), _user=Depends(get_current_user)
):
    bal = db.query(models.LeaveBalance).filter(
        models.LeaveBalance.employee_id == employee_id
    ).first()
    if not bal:
        raise HTTPException(status_code=404, detail="Leave balance not found")
    return bal


@router.put("/{employee_id}/balance", response_model=schemas.LeaveBalanceOut)
def update_balance(
    employee_id: str,
    payload: schemas.LeaveBalanceUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_role("HR Admin", "Super Admin")),
):
    bal = db.query(models.LeaveBalance).filter(
        models.LeaveBalance.employee_id == employee_id
    ).first()
    if not bal:
        raise HTTPException(status_code=404, detail="Leave balance not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(bal, field, value)
    db.commit()
    db.refresh(bal)
    return bal
