"""
seed_data.py
-------------
Populates the database with realistic demo data so the portal looks
alive the moment you log in, instead of an empty shell.

Run with:  cd backend && python seed_data.py
Safe to re-run -- it wipes and recreates all tables first.

Demo login credentials (all passwords: Demo@123):
  superadmin   -> Super Admin
  priya.hr     -> HR Admin
  arjun.mgr    -> Manager (Engineering)
  meera.mgr    -> Manager (Sales)
  rahul.dev    -> Employee (Engineering)
  ...see printed table at the end of this script for the full list.
"""

from datetime import date, timedelta
import random

from database import Base, engine, SessionLocal
import models
from auth import hash_password

# ---------------------------------------------------------------------
# 1. Reset schema
# ---------------------------------------------------------------------
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ---------------------------------------------------------------------
# 2. Departments
# ---------------------------------------------------------------------
department_names = ["Engineering", "Sales", "Marketing", "Human Resources", "Finance", "Operations"]
for name in department_names:
    db.add(models.Department(department_name=name))
db.commit()

# ---------------------------------------------------------------------
# 3. Employees (id, name, email, department, manager_id, joining_date)
#    Managers are listed first so their employee_id exists before being
#    referenced as a "manager" value on the staff below them.
# ---------------------------------------------------------------------
employees = [
    # Leadership / managers
    ("EMP001", "Arjun Mehta",  "arjun.mehta@company.com",  "Engineering",     None,     "2018-03-01"),
    ("EMP002", "Meera Iyer",   "meera.iyer@company.com",   "Sales",           None,     "2017-06-15"),
    ("EMP003", "Karthik Rao",  "karthik.rao@company.com",  "Marketing",       None,     "2019-01-10"),
    ("EMP004", "Divya Nair",   "divya.nair@company.com",   "Finance",         None,     "2016-09-20"),

    # HR Admin
    ("EMP010", "Priya Sharma", "priya.sharma@company.com", "Human Resources", None,     "2015-05-05"),

    # Engineering team
    ("EMP101", "Rahul Verma",  "rahul.verma@company.com",  "Engineering",     "EMP001", "2021-07-12"),
    ("EMP102", "Sneha Gupta",  "sneha.gupta@company.com",  "Engineering",     "EMP001", "2022-02-18"),
    ("EMP103", "Vikram Singh", "vikram.singh@company.com", "Engineering",     "EMP001", "2020-11-03"),
    ("EMP104", "Ananya Das",   "ananya.das@company.com",   "Engineering",     "EMP001", "2023-01-09"),

    # Sales team
    ("EMP201", "Rohan Kapoor", "rohan.kapoor@company.com", "Sales",           "EMP002", "2021-04-22"),
    ("EMP202", "Pooja Reddy",  "pooja.reddy@company.com",  "Sales",           "EMP002", "2022-08-30"),
    ("EMP203", "Aditya Joshi", "aditya.joshi@company.com", "Sales",           "EMP002", "2020-06-14"),

    # Marketing team
    ("EMP301", "Kavya Pillai", "kavya.pillai@company.com", "Marketing",       "EMP003", "2022-03-25"),
    ("EMP302", "Nikhil Bose",  "nikhil.bose@company.com",  "Marketing",       "EMP003", "2021-10-11"),

    # Finance team
    ("EMP401", "Shreya Menon", "shreya.menon@company.com", "Finance",         "EMP004", "2019-12-02"),
    ("EMP402", "Varun Chawla", "varun.chawla@company.com", "Finance",         "EMP004", "2023-05-19"),

    # Operations (no dedicated manager seeded -- reports straight to HR for this demo)
    ("EMP501", "Ishita Kohli", "ishita.kohli@company.com", "Operations",      "EMP010", "2022-09-07"),
    ("EMP502", "Manish Tiwari","manish.tiwari@company.com","Operations",      "EMP010", "2021-02-28"),
]

for emp_id, name, email, dept, manager, joined in employees:
    db.add(models.Employee(
        employee_id=emp_id,
        employee_name=name,
        email=email,
        department=dept,
        manager=manager,
        joining_date=date.fromisoformat(joined),
        status="Active",
    ))
    # Default leave balance for every employee
    db.add(models.LeaveBalance(employee_id=emp_id))
db.commit()

# ---------------------------------------------------------------------
# 4. Users / logins
#    username, role, employee_id, full_name
# ---------------------------------------------------------------------
DEMO_PASSWORD = "Demo@123"

users = [
    ("superadmin", "Super Admin", None,     "System Administrator"),
    ("priya.hr",   "HR Admin",    "EMP010", "Priya Sharma"),
    ("arjun.mgr",  "Manager",     "EMP001", "Arjun Mehta"),
    ("meera.mgr",  "Manager",     "EMP002", "Meera Iyer"),
    ("karthik.mgr","Manager",     "EMP003", "Karthik Rao"),
    ("divya.mgr",  "Manager",     "EMP004", "Divya Nair"),
    ("rahul.dev",  "Employee",    "EMP101", "Rahul Verma"),
    ("sneha.dev",  "Employee",    "EMP102", "Sneha Gupta"),
    ("vikram.dev", "Employee",    "EMP103", "Vikram Singh"),
    ("rohan.sales","Employee",    "EMP201", "Rohan Kapoor"),
    ("kavya.mktg", "Employee",    "EMP301", "Kavya Pillai"),
    ("shreya.fin", "Employee",    "EMP401", "Shreya Menon"),
]

for username, role, emp_id, full_name in users:
    db.add(models.User(
        username=username,
        password_hash=hash_password(DEMO_PASSWORD),
        role=role,
        employee_id=emp_id,
        full_name=full_name,
    ))
db.commit()

# ---------------------------------------------------------------------
# 5. Holidays (India-centric public/regional/company mix for 2026)
# ---------------------------------------------------------------------
holidays = [
    ("New Year's Day",        "2026-01-01", "Public"),
    ("Republic Day",          "2026-01-26", "Public"),
    ("Holi",                  "2026-03-04", "Regional"),
    ("Good Friday",           "2026-04-03", "Regional"),
    ("Independence Day",      "2026-08-15", "Public"),
    ("Ganesh Chaturthi",      "2026-09-14", "Regional"),
    ("Gandhi Jayanti",        "2026-10-02", "Public"),
    ("Diwali",                "2026-11-08", "Public"),
    ("Company Foundation Day","2026-11-20", "Company"),
    ("Christmas",             "2026-12-25", "Public"),
]
for name, hdate, htype in holidays:
    db.add(models.Holiday(
        holiday_name=name, holiday_date=date.fromisoformat(hdate), holiday_type=htype
    ))
db.commit()

# ---------------------------------------------------------------------
# 6. Sample leave requests, spread across the year so dashboard charts
#    have something to show (mix of Approved / Pending / Rejected).
# ---------------------------------------------------------------------
leave_types_pool = [
    "Casual Leave", "Sick Leave", "Earned Leave", "Work From Home",
    "Half Day Leave", "Compensatory Off",
]
reasons_pool = [
    "Personal work", "Family function", "Not feeling well", "Festival travel",
    "Medical appointment", "Home repairs", "Wedding in family", "Short trip",
]

random.seed(42)  # deterministic demo data
today = date.today()
staff_only = [e for e in employees if e[0] not in ("EMP001", "EMP002", "EMP003", "EMP004", "EMP010")]

sample_requests = []
for i in range(40):
    emp_id, name, email, dept, manager, joined = random.choice(staff_only)
    leave_type = random.choice(leave_types_pool)
    start_offset = random.randint(-150, 20)  # spread across recent months, a few upcoming
    start = today + timedelta(days=start_offset)
    duration = 0 if leave_type == "Half Day Leave" else random.randint(0, 3)
    end = start + timedelta(days=duration)
    status = random.choices(["Approved", "Pending", "Rejected"], weights=[60, 25, 15])[0]
    sample_requests.append(models.LeaveRequest(
        employee_id=emp_id,
        leave_type=leave_type,
        start_date=start,
        end_date=end,
        reason=random.choice(reasons_pool),
        emergency_contact="+91-90000-00000",
        status=status,
        manager_comments="Approved, enjoy!" if status == "Approved" else (
            "Cannot release the team during this sprint" if status == "Rejected" else None
        ),
    ))

db.add_all(sample_requests)
db.commit()

# Manually deduct balances for the Approved sample requests so the
# progress bars on the dashboard look realistic instead of always-full
for req in sample_requests:
    if req.status != "Approved":
        continue
    field = {"Casual Leave": "casual_leave", "Sick Leave": "sick_leave", "Earned Leave": "annual_leave"}.get(req.leave_type)
    if not field:
        continue
    bal = db.query(models.LeaveBalance).filter(models.LeaveBalance.employee_id == req.employee_id).first()
    days = (req.end_date - req.start_date).days + 1
    current = getattr(bal, field)
    setattr(bal, field, max(current - days, 0))
db.commit()

db.close()

# ---------------------------------------------------------------------
print("\n✅  Database seeded successfully: leave_management.db")
print(f"\n{'USERNAME':<14}{'ROLE':<14}{'PASSWORD'}")
print("-" * 42)
for username, role, _, _ in users:
    print(f"{username:<14}{role:<14}{DEMO_PASSWORD}")
print("\nLog in with any of the above at the Streamlit app's login screen.\n")
