"""
schemas.py
----------
Pydantic models used for request validation and response shaping.
Keeping these separate from the SQLAlchemy models in models.py is standard
FastAPI practice -- DB shape and API shape are allowed to drift slightly.
"""

from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional


# ---------- Auth ----------

class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str
    employee_id: Optional[str] = None


# ---------- Department ----------

class DepartmentCreate(BaseModel):
    department_name: str


class DepartmentOut(BaseModel):
    department_id: int
    department_name: str

    class Config:
        from_attributes = True


# ---------- Employee ----------

class EmployeeCreate(BaseModel):
    employee_id: str
    employee_name: str
    email: EmailStr
    department: str
    manager: Optional[str] = None
    joining_date: date
    status: str = "Active"
    # Optional login creation alongside the employee record
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = "Employee"


class EmployeeUpdate(BaseModel):
    employee_name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    manager: Optional[str] = None
    status: Optional[str] = None


class EmployeeOut(BaseModel):
    employee_id: str
    employee_name: str
    email: str
    department: Optional[str]
    manager: Optional[str]
    joining_date: date
    status: str

    class Config:
        from_attributes = True


# ---------- Leave Balance ----------

class LeaveBalanceOut(BaseModel):
    employee_id: str
    annual_leave: int
    sick_leave: int
    casual_leave: int

    class Config:
        from_attributes = True


class LeaveBalanceUpdate(BaseModel):
    annual_leave: Optional[int] = None
    sick_leave: Optional[int] = None
    casual_leave: Optional[int] = None


# ---------- Leave Request ----------

class LeaveRequestCreate(BaseModel):
    employee_id: str
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None
    emergency_contact: Optional[str] = None


class LeaveRequestDecision(BaseModel):
    status: str  # Approved / Rejected / Clarification Requested
    manager_comments: Optional[str] = None


class LeaveRequestOut(BaseModel):
    leave_id: int
    employee_id: str
    employee_name: Optional[str] = None
    department: Optional[str] = None
    leave_type: str
    start_date: date
    end_date: date
    days_requested: int
    reason: Optional[str]
    emergency_contact: Optional[str]
    status: str
    manager_comments: Optional[str]
    applied_on: datetime

    class Config:
        from_attributes = True


# ---------- Holiday ----------

class HolidayCreate(BaseModel):
    holiday_name: str
    holiday_date: date
    holiday_type: str = "Public"


class HolidayOut(BaseModel):
    holiday_id: int
    holiday_name: str
    holiday_date: date
    holiday_type: str

    class Config:
        from_attributes = True


# ---------- Notifications ----------

class NotificationOut(BaseModel):
    notification_id: int
    message: str
    leave_id: Optional[int] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Dashboard ----------

class DashboardSummary(BaseModel):
    total_employees: int
    present_today: int
    on_leave_today: int
    pending_requests: int
    approved_leaves: int
    rejected_leaves: int
    upcoming_holidays: int
    leave_utilization_pct: float
