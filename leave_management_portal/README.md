# Leave Management Portal

**Smart Leave Planning. Seamless Workforce Management.**

A full-stack enterprise leave management system: FastAPI backend (JWT auth,
SQLAlchemy ORM, SQLite) + Streamlit frontend (glassmorphism UI, Plotly
charts, dark/light mode).

---

## 1. Setup (one-time)

Requires Python 3.10+ (built and checked against 3.12).

```bash
cd leave_management_portal
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> On Apple Silicon Macs, bcrypt installs from a prebuilt wheel — no
> compiler step needed. If you ever hit a build error, run
> `pip install --upgrade pip` first and retry.

## 2. Run it

Two terminals, both with the venv active:

```bash
# Terminal 1 — backend (also seeds demo data on first run)
./start_backend.sh

# Terminal 2 — frontend
./start_frontend.sh
```

Open **http://localhost:8501**. The backend API + interactive docs are at
**http://127.0.0.1:8000/docs**.

To re-seed from scratch at any point: `cd backend && python3 seed_data.py`
(this drops and recreates all tables).

## 3. Demo logins

All demo accounts use the password **`Demo@123`**.

| Username      | Role        | Notes                          |
|---------------|-------------|---------------------------------|
| `superadmin`  | Super Admin | Full system access              |
| `priya.hr`    | HR Admin    | Employee/department/holiday mgmt|
| `arjun.mgr`   | Manager     | Engineering team, has reports   |
| `meera.mgr`   | Manager     | Sales team                      |
| `rahul.dev`   | Employee    | Engineering, has leave history  |

(Full list printed by `seed_data.py` when it runs.)

## 4. Project structure

```
leave_management_portal/
├── backend/
│   ├── main.py            FastAPI app + router wiring + CORS
│   ├── database.py        SQLAlchemy engine/session
│   ├── models.py          ORM models (6 tables)
│   ├── schemas.py         Pydantic request/response shapes
│   ├── auth.py            JWT + bcrypt + RBAC dependency
│   ├── seed_data.py       Demo data generator
│   └── routers/
│       ├── auth_routes.py
│       ├── employees.py
│       ├── departments.py
│       ├── holidays.py
│       ├── leaves.py
│       ├── dashboard.py
│       └── reports.py
├── frontend/
│   ├── app.py              Entry point: nav shell, routing, theme
│   ├── styles.py            CSS tokens + glassmorphism components
│   ├── api_client.py        Thin requests wrapper w/ auth header
│   └── pages/
│       ├── landing.py
│       ├── auth_page.py
│       ├── dashboard_page.py
│       ├── employee_portal_page.py
│       ├── manager_approvals_page.py
│       ├── hr_admin_page.py
│       └── reports_page.py
├── requirements.txt
├── start_backend.sh
└── start_frontend.sh
```

## 5. What's fully working

- **Landing page** — hero, stats, features, testimonials, pricing, footer
- **Auth** — JWT login, bcrypt password hashing, role-based access control
  enforced at the API layer (UI also hides actions a role can't take)
- **Executive Dashboard** — 8 KPI cards, monthly trend, leave-type donut,
  department bar chart, all from live DB data
- **Employee Self-Service** — apply leave (with overlap/conflict detection
  against the employee's own requests), leave balance progress bars,
  full request history
- **Manager Approval Center** — team requests, approve/reject/request
  clarification with comments, team-availability check for the requested dates
- **HR Administration** — employee CRUD (with optional login creation),
  department CRUD, holiday calendar CRUD
- **Reports** — Leave Summary, Attendance Analysis, Employee Directory,
  each exportable to CSV and Excel
- **Dark / light mode toggle**, role-gated sidebar navigation, a basic
  in-app notification popover

## 6. Documented scope decisions (read before extending)

- **Leave balance deduction** only applies to Casual / Sick / Earned Leave,
  and only on manager **approval** (not at apply time). Maternity,
  Paternity, WFH, Compensatory Off, and Half Day Leave are tracked and
  approved but don't draw down a numeric balance bucket — there's no
  natural 1:1 mapping for those onto the three balance columns in the spec.
- **File attachments** on the Apply Leave form are accepted by the UI but
  not yet persisted to disk/DB.
- **CORS middleware** is enabled on the API for future-proofing, but since
  Streamlit calls FastAPI server-side (Python `requests`, not browser
  `fetch`), it isn't actually load-bearing in this architecture today.

## 7. Not built yet (flagged rather than faked)

These were in the original spec but would need real scope/time to do
properly rather than stub:

- Bulk employee upload (CSV import)
- PDF report export (CSV/Excel are done)
- Real email notifications (the in-app notification popover works; SMTP
  isn't wired up)
- Audit logs
- Automated leave-conflict detection across teams (today's conflict check
  is per-employee; the Manager's "also off in this window" note covers
  the cross-employee case for the dates being decided)
- Leave forecasting / workforce planning analytics

Happy to build out any of these next — just say which one.
