"""
pages/reports_page.py
------------------------
Reports & Analytics: pulls data from the /api/reports/* endpoints and
lets HR/Managers export it as CSV or Excel. PDF export is flagged as a
next-phase item rather than half-built.
"""

import streamlit as st
import pandas as pd
from io import BytesIO

import api_client


def _download_buttons(df: pd.DataFrame, filename_base: str):
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "⬇️ Download CSV", data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"{filename_base}.csv", mime="text/csv", use_container_width=True,
        )
    with c2:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Report")
        st.download_button(
            "⬇️ Download Excel", data=buffer.getvalue(), file_name=f"{filename_base}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )


def render():
    st.markdown("### 📈 Reports & Analytics")
    st.caption("PDF export and automated leave-forecasting are planned for a future phase.")

    report_choice = st.selectbox(
        "Choose a report",
        ["Leave Summary", "Attendance Analysis", "Employee Directory"],
    )

    if report_choice == "Leave Summary":
        departments = api_client.get("/api/departments")
        dept_names = ["All"] + [d["department_name"] for d in departments] if departments else ["All"]
        c1, c2 = st.columns(2)
        with c1:
            dept_filter = st.selectbox("Department", dept_names)
        with c2:
            status_filter = st.selectbox("Status", ["All", "Pending", "Approved", "Rejected"])

        params = {}
        if dept_filter != "All":
            params["department"] = dept_filter
        if status_filter != "All":
            params["status_filter"] = status_filter

        data = api_client.get("/api/reports/leave-summary", params=params)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            _download_buttons(df, "leave_summary")
        else:
            st.info("No records match these filters.")

    elif report_choice == "Attendance Analysis":
        data = api_client.get("/api/reports/attendance-analysis")
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            _download_buttons(df, "attendance_analysis")
        else:
            st.info("No data available yet.")

    elif report_choice == "Employee Directory":
        data = api_client.get("/api/reports/employee-directory")
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            _download_buttons(df, "employee_directory")
        else:
            st.info("No employees found.")
