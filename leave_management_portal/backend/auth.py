"""
auth.py
-------
Password hashing (bcrypt) + JWT issuing/verification + the
get_current_user / require_role FastAPI dependencies used to enforce
Role Based Access Control (RBAC) across the API.

Roles: Employee, Manager, HR Admin, Super Admin
"""

import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
import models

# --- Config -----------------------------------------------------------
# In a real deployment this secret must come from an environment
# variable, never be hardcoded, and be rotated. Kept simple for the
# course project.
SECRET_KEY = "leave-management-portal-secret-key-change-me"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 8  # 8-hour session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# --- Password hashing ---------------------------------------------------

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), password_hash.encode())


# --- JWT -----------------------------------------------------------------

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired, please log in again")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")


# --- Dependencies ----------------------------------------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    payload = decode_access_token(token)
    username = payload.get("sub")
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_role(*allowed_roles: str):
    """
    Usage: Depends(require_role("Manager", "HR Admin", "Super Admin"))
    """
    def role_checker(current_user: models.User = Depends(get_current_user)) -> models.User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' is not permitted to perform this action",
            )
        return current_user
    return role_checker
