"""
models.py
---------
SQLAlchemy ORM models for the Leave Management Portal.

Tables: Employees, LeaveRequests, LeaveBalance, Departments, Holidays, Users

Note on LeaveBalance: the spec's three balance buckets (annual / sick / casual)
don't map 1:1 onto all 8 leave types (e.g. Maternity, Paternity, WFH,
Compensatory Off, Half Day). Those policy-driven types are tracked and
approved through LeaveRequests but don't deduct from a numeric balance --
that's a reasonable assumption for an MVP; flagging it so it's not a silent
choice.
"""

from sqlalchemy import (
     Column, Integer, String, Date, DateTime, ForeignKey, Text, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String, unique=True, nullable=False)

    employees = relationship("Employee", back_populates="department_obj")


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(String, primary_key=True)          # e.g. "EMP001"
    employee_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department = Column(String, ForeignKey("departments.department_name"))
    manager = Column(String, nullable=True)                 # manager's employee_id
    joining_date = Column(Date, nullable=False)
    status = Column(String, default="Active")               # Active / Inactive

    department_obj = relationship("Department", back_populates="employees")
    leave_requests = relationship("LeaveRequest", back_populates="employee")
    balance = relationship("LeaveBalance", back_populates="employee", uselist=False)


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    leave_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String, ForeignKey("employees.employee_id"), nullable=False)
    leave_type = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=True)
    emergency_contact = Column(String, nullable=True)
    attachment_path = Column(String, nullable=True)
    status = Column(String, default="Pending")              # Pending/Approved/Rejected
    manager_comments = Column(Text, nullable=True)
    applied_on = Column(DateTime, server_default=func.now())

    employee = relationship("Employee", back_populates="leave_requests")


class LeaveBalance(Base):
    __tablename__ = "leave_balance"

    employee_id = Column(String, ForeignKey("employees.employee_id"), primary_key=True)
    annual_leave = Column(Integer, default=18)
    sick_leave = Column(Integer, default=10)
    casual_leave = Column(Integer, default=8)

    employee = relationship("Employee", back_populates="balance")


class Holiday(Base):
    __tablename__ = "holidays"

    holiday_id = Column(Integer, primary_key=True, autoincrement=True)
    holiday_name = Column(String, nullable=False)
    holiday_date = Column(Date, nullable=False)
    holiday_type = Column(String, default="Public")  # Public / Regional / Company


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # Employee / Manager / HR Admin / Super Admin
    employee_id = Column(String, ForeignKey("employees.employee_id"), nullable=True)
    full_name = Column(String, nullable=False)
class Notification(Base):
    """
    Created in two places (see routers/leaves.py):
      - when an employee applies for leave -> notifies their manager
      - when a manager decides on a request -> notifies the employee
    recipient_username points at Users.username so the bell icon can
    just ask "what's mine" using the logged-in user's own username.
    """
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    recipient_username = Column(String, ForeignKey("users.username"), nullable=False)
    message = Column(Text, nullable=False)
    leave_id = Column(Integer, ForeignKey("leave_requests.leave_id"), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())