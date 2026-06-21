"""
pages/employee_portal_page.py
--------------------------------
Employee Self-Service Portal: Apply Leave form and My Leave Dashboard
(balance progress bars + request history).
"""

import streamlit as st
import pandas as pd
from datetime import date

import api_client
from styles import balance_bar, badge, COLORS

LEAVE_TYPES = [
    "Casual Leave", "Sick Leave", "Earned Leave", "Maternity Leave",
    "Paternity Leave", "Compensatory Off", "Work From Home", "Half Day Leave",
]

STATUS_BADGE = {"Approved": "success", "Pending": "warning", "Rejected": "danger",
                "Clarification Requested": "info"}


def render_apply_leave():
    st.markdown("### 📅 Apply for Leave")
    emp_id = st.session_state.employee_id

    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Employee ID", value=emp_id, disabled=True)
        with c2:
            st.text_input("Employee Name", value=st.session_state.full_name, disabled=True)

        leave_type = st.selectbox("Leave Type", LEAVE_TYPES)
        c3, c4 = st.columns(2)
        with c3:
            start = st.date_input("Start Date", value=date.today())
        with c4:
            end = st.date_input("End Date", value=date.today())

        reason = st.text_area("Reason", placeholder="Briefly describe the reason for leave")
        emergency_contact = st.text_input("Emergency Contact", placeholder="+91-XXXXX-XXXXX")
        st.file_uploader(
            "Attachment (optional)", type=["pdf", "jpg", "png"],
            help="Medical certificate, travel proof, etc. Storage isn't wired up in this build -- "
                 "the file is accepted but not yet persisted."
        )

        if st.button("Submit Leave Request", use_container_width=True):
            if end < start:
                st.error("End date cannot be before start date.")
            else:
                payload = {
                    "employee_id": emp_id,
                    "leave_type": leave_type,
                    "start_date": str(start),
                    "end_date": str(end),
                    "reason": reason,
                    "emergency_contact": emergency_contact,
                }
                result = api_client.post("/api/leaves", payload)
                if result:
                    st.success(f"Leave request #{result['leave_id']} submitted and is now Pending approval.")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def render_my_dashboard():
    st.markdown("### 🗂️ My Leave Dashboard")
    emp_id = st.session_state.employee_id

    balance = api_client.get(f"/api/employees/{emp_id}/balance")
    requests_list = api_client.get("/api/leaves/my")

    st.markdown("#### Leave Balance")
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        balance_bar("Annual Leave", 18 - balance["annual_leave"], 18, COLORS["primary"])
        balance_bar("Sick Leave", 10 - balance["sick_leave"], 10, COLORS["danger"])
        balance_bar("Casual Leave", 8 - balance["casual_leave"], 8, COLORS["secondary"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    pending = [r for r in requests_list if r["status"] == "Pending"]
    approved = [r for r in requests_list if r["status"] == "Approved"]
    rejected = [r for r in requests_list if r["status"] == "Rejected"]
    upcoming = [r for r in approved if r["start_date"] >= str(date.today())]

    summary_cols = st.columns(4)
    labels = [("Pending", len(pending), COLORS["warning"]), ("Approved", len(approved), COLORS["success"]),
              ("Rejected", len(rejected), COLORS["danger"]), ("Upcoming", len(upcoming), COLORS["primary"])]
    for col, (label, count, color) in zip(summary_cols, labels):
        with col:
            st.markdown(f"""
                <div class="glass-card" style="text-align:center; border-left:4px solid {color};">
                    <div class="kpi-value" style="font-size:1.5rem;">{count}</div>
                    <div class="kpi-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.markdown("#### Request History")

    if not requests_list:
        st.info("No leave requests yet. Apply for one from the Apply Leave tab.")
        return

    for r in requests_list:
        status_class = STATUS_BADGE.get(r["status"], "info")
        st.markdown(f"""
            <div class="glass-card" style="margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <strong>{r['leave_type']}</strong>
                        &nbsp;·&nbsp; {r['start_date']} → {r['end_date']}
                        &nbsp;·&nbsp; {r['days_requested']} day(s)
                    </div>
                    {badge(r['status'], status_class)}
                </div>
                <div style="color:var(--text-muted); font-size:0.85rem; margin-top:6px;">
                    {r['reason'] or '—'}
                </div>
                {f'<div style="font-size:0.82rem; margin-top:6px;"><em>Manager note: {r["manager_comments"]}</em></div>' if r['manager_comments'] else ''}
            </div>
        """, unsafe_allow_html=True)


def render():
    tab1, tab2 = st.tabs(["📅 Apply Leave", "🗂️ My Leave Dashboard"])
    with tab1:
        render_apply_leave()
    with tab2:
        render_my_dashboard()
