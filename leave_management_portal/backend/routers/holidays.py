"""
routers/holidays.py
---------------------
Holiday calendar management. Read is open to all logged-in users
(employees need to see the calendar); writes are HR Admin / Super Admin only.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from database import get_db
from auth import get_current_user, require_role
import models
import schemas

router = APIRouter(prefix="/api/holidays", tags=["Holidays"])


@router.get("", response_model=List[schemas.HolidayOut])
def list_holidays(
    upcoming_only: bool = False,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = db.query(models.Holiday)
    if upcoming_only:
        query = query.filter(models.Holiday.holiday_date >= date.today())
    return query.order_by(models.Holiday.holiday_date).all()


@router.post("", response_model=schemas.HolidayOut)
def create_holiday(
    payload: schemas.HolidayCreate,
    db: Session = Depends(get_db),
    _user=Depends(require_role("HR Admin", "Super Admin")),
):
    holiday = models.Holiday(**payload.model_dump())
    db.add(holiday)
    db.commit()
    db.refresh(holiday)
    return holiday


@router.delete("/{holiday_id}")
def delete_holiday(
    holiday_id: int,
    db: Session = Depends(get_db),
    _user=Depends(require_role("HR Admin", "Super Admin")),
):
    holiday = db.query(models.Holiday).filter(models.Holiday.holiday_id == holiday_id).first()
    if not holiday:
        raise HTTPException(status_code=404, detail="Holiday not found")
    db.delete(holiday)
    db.commit()
    return {"detail": "Holiday deleted"}
