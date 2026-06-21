"""
routers/notifications.py
--------------------------
Reads the Notification rows created in routers/leaves.py:
  - apply_leave()  -> notifies the employee's manager
  - decide_leave() -> notifies the employee

Each user only ever sees their own notifications (filtered by their
own username, taken from the JWT via get_current_user).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from auth import get_current_user
import models
import schemas

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("", response_model=List[schemas.NotificationOut])
def list_notifications(
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.Notification).filter(
        models.Notification.recipient_username == current_user.username
    )
    if unread_only:
        query = query.filter(models.Notification.is_read == False)
    return query.order_by(models.Notification.created_at.desc()).limit(20).all()


@router.get("/unread-count")
def unread_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    count = db.query(models.Notification).filter(
        models.Notification.recipient_username == current_user.username,
        models.Notification.is_read == False,
    ).count()
    return {"unread_count": count}


@router.post("/{notification_id}/read", response_model=schemas.NotificationOut)
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    note = db.query(models.Notification).filter(
        models.Notification.notification_id == notification_id,
        models.Notification.recipient_username == current_user.username,
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Notification not found")
    note.is_read = True
    db.commit()
    db.refresh(note)
    return note


@router.post("/mark-all-read")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db.query(models.Notification).filter(
        models.Notification.recipient_username == current_user.username,
        models.Notification.is_read == False,
    ).update({"is_read": True})
    db.commit()
    return {"detail": "All notifications marked as read"}