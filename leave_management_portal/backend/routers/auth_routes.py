"""
routers/auth_routes.py
-----------------------
Login endpoint. Issues a JWT containing the username, role and
linked employee_id so the frontend can route/gate by role without
extra round trips.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from auth import verify_password, create_access_token
import models
import schemas

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.LoginResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(
        {"sub": user.username, "role": user.role, "employee_id": user.employee_id}
    )
    return schemas.LoginResponse(
        access_token=token,
        role=user.role,
        full_name=user.full_name,
        employee_id=user.employee_id,
    )
