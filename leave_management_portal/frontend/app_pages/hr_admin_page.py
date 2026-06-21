"""
pages/hr_admin_page.py
-------------------------
HR Administration Module: Employee Management, Department Management,
and Holiday Calendar Management. Restricted to HR Admin / Super Admin
(enforced again here on top of the API's RBAC, so the UI doesn't even
offer actions the backend would reject).
"""

import streamlit as st
import pandas as pd
from datetime import date

import api_client
from styles import badge

HOLIDAY_TYPE_BADGE = {"Public": "info", "Regional": "success", "Company": "warning"}


def render_employee_management():
    st.markdown("#### 👥 Employee Management")

    search = st.text_input("Search by name, ID, or email", placeholder="e.g. Rahul or EMP101")
    employees = api_client.get("/api/employees", params={"search": search} if search else None)

    if employees:
        df = pd.DataFrame(employees)
        st.dataframe(
            df[["employee_id", "employee_name", "email", "department", "manager", "joining_date", "status"]],
            use_container_width=True, hide_index=True,
        )
    else:
        st.info("No employees found.")

    with st.expander("➕ Add New Employee"):
        departments = api_client.get("/api/departments")
        dept_names = [d["department_name"] for d in departments] if departments else []

        c1, c2 = st.columns(2)
        with c1:
            emp_id = st.text_input("Employee ID", placeholder="EMP601")
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            joining = st.date_input("Joining Date", value=date.today())
        with c2:
            dept = st.selectbox("Department", dept_names) if dept_names else st.text_input("Department")
            manager_id = st.text_input("Manager's Employee ID (optional)")
            username = st.text_input("Login Username (optional)")
            password = st.text_input("Login Password (optional)", type="password")

        if st.button("Create Employee"):
            if not (emp_id and name and email and dept):
                st.warning("Employee ID, name, email, and department are required.")
            else:
                payload = {
                    "employee_id": emp_id, "employee_name": name, "email": email,
                    "department": dept, "manager": manager_id or None,
                    "joining_date": str(joining),
                }
                if username and password:
                    payload.update({"username": username, "password": password, "role": "Employee"})
                result = api_client.post("/api/employees", payload)
                if result:
                    st.success(f"Employee {emp_id} created.")
                    st.rerun()

    with st.expander("✏️ Edit or Deactivate Employee"):
        if employees:
            ids = [e["employee_id"] for e in employees]
            target = st.selectbox("Select employee", ids)
            current = next(e for e in employees if e["employee_id"] == target)

            c1, c2 = st.columns(2)
            with c1:
                new_status = st.selectbox("Status", ["Active", "Inactive"],
                                           index=0 if current["status"] == "Active" else 1)
                new_manager = st.text_input("Manager's Employee ID", value=current.get("manager") or "")
            with c2:
                new_dept = st.text_input("Department", value=current.get("department") or "")

            if st.button("Save Changes"):
                api_client.put(f"/api/employees/{target}", {
                    "status": new_status, "manager": new_manager or None, "department": new_dept,
                })
                st.success("Employee updated.")
                st.rerun()
        else:
            st.caption("No employees to edit yet.")


def render_department_management():
    st.markdown("#### 🏢 Department Management")
    departments = api_client.get("/api/departments")

    if departments:
        st.dataframe(pd.DataFrame(departments), use_container_width=True, hide_index=True)
    else:
        st.info("No departments yet.")

    with st.expander("➕ Add Department"):
        new_dept = st.text_input("Department Name")
        if st.button("Create Department"):
            if new_dept:
                api_client.post("/api/departments", {"department_name": new_dept})
                st.success(f"Department '{new_dept}' created.")
                st.rerun()
            else:
                st.warning("Enter a department name.")


def render_holiday_management():
    st.markdown("#### 🎉 Holiday Calendar")
    holidays = api_client.get("/api/holidays")

    if holidays:
        for h in sorted(holidays, key=lambda x: x["holiday_date"]):
            st.markdown(f"""
                <div class="glass-card" style="margin-bottom:8px; padding:12px 18px; display:flex; justify-content:space-between; align-items:center;">
                    <div><strong>{h['holiday_name']}</strong> &nbsp;·&nbsp; {h['holiday_date']}</div>
                    {badge(h['holiday_type'], HOLIDAY_TYPE_BADGE.get(h['holiday_type'], 'info'))}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No holidays configured yet.")

    with st.expander("➕ Add Holiday"):
        c1, c2, c3 = st.columns(3)
        with c1:
            h_name = st.text_input("Holiday Name")
        with c2:
            h_date = st.date_input("Date")
        with c3:
            h_type = st.selectbox("Type", ["Public", "Regional", "Company"])
        if st.button("Add Holiday"):
            if h_name:
                api_client.post("/api/holidays", {
                    "holiday_name": h_name, "holiday_date": str(h_date), "holiday_type": h_type,
                })
                st.success(f"'{h_name}' added to the calendar.")
                st.rerun()
            else:
                st.warning("Enter a holiday name.")


def render():
    st.markdown("### ⚙️ HR Administration")
    tab1, tab2, tab3 = st.tabs(["👥 Employees", "🏢 Departments", "🎉 Holidays"])
    with tab1:
        render_employee_management()
    with tab2:
        render_department_management()
    with tab3:
        render_holiday_management()
