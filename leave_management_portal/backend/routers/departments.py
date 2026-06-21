"""
routers/departments.py
------------------------
CRUD for departments. Read is open to any logged-in user (needed to
populate dropdowns); writes are restricted to HR Admin / Super Admin.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from auth import get_current_user, require_role
import models
import schemas

router = APIRouter(prefix="/api/departments", tags=["Departments"])


@router.get("", response_model=List[schemas.DepartmentOut])
def list_departments(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return db.query(models.Department).order_by(models.Department.department_name).all()


@router.post("", response_model=schemas.DepartmentOut)
def create_department(
    payload: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
    _user=Depends(require_role("HR Admin", "Super Admin")),
):
    existing = db.query(models.Department).filter(
        models.Department.department_name == payload.department_name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department already exists")
    dept = models.Department(department_name=payload.department_name)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    _user=Depends(require_role("HR Admin", "Super Admin")),
):
    dept = db.query(models.Department).filter(
        models.Department.department_id == department_id
    ).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(dept)
    db.commit()
    return {"detail": "Department deleted"}
