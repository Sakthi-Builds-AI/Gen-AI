"""
pages/dashboard_page.py
-------------------------
Executive Dashboard: the 8 KPI cards plus monthly trend, department
breakdown, and leave-type distribution charts.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

import api_client
from styles import kpi_card, COLORS

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def render():
    st.markdown("## 📊 Executive Dashboard")
    st.caption(f"Welcome back, {st.session_state.get('full_name', '')} · {st.session_state.get('role', '')}")

    summary = api_client.get("/api/dashboard/summary")

    row1 = st.columns(4)
    with row1[0]:
        kpi_card("👥", "Total Employees", summary["total_employees"], COLORS["primary"])
    with row1[1]:
        kpi_card("🟢", "Present Today", summary["present_today"], COLORS["success"])
    with row1[2]:
        kpi_card("🌴", "On Leave Today", summary["on_leave_today"], COLORS["warning"])
    with row1[3]:
        kpi_card("⏳", "Pending Requests", summary["pending_requests"], COLORS["accent"])

    row2 = st.columns(4)
    with row2[0]:
        kpi_card("✅", "Approved Leaves", summary["approved_leaves"], COLORS["success"])
    with row2[1]:
        kpi_card("❌", "Rejected Leaves", summary["rejected_leaves"], COLORS["danger"])
    with row2[2]:
        kpi_card("🎉", "Upcoming Holidays", summary["upcoming_holidays"], COLORS["secondary"])
    with row2[3]:
        kpi_card("📈", "Leave Utilization", f"{summary['leave_utilization_pct']}%", COLORS["primary_light"])

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns([1.4, 1])

    # ---- Monthly trend ----
    with chart_col1:
        st.markdown("#### Monthly Leave Trend")
        trend = api_client.get("/api/dashboard/monthly-trend")
        trend_map = {int(r["month"]): r["count"] for r in trend}
        x = MONTH_NAMES
        y = [trend_map.get(m, 0) for m in range(1, 13)]
        fig = go.Figure(go.Scatter(
            x=x, y=y, mode="lines+markers", line=dict(color=COLORS["primary"], width=3, shape="spline"),
            marker=dict(size=7, color=COLORS["primary_light"]), fill="tozeroy",
            fillcolor="rgba(37,99,235,0.10)",
        ))
        fig.update_layout(
            height=320, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)"),
            font=dict(color=st.session_state.get("chart_text_color", "#64748B")),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---- Leave type donut ----
    with chart_col2:
        st.markdown("#### Leave Type Mix")
        type_breakdown = api_client.get("/api/dashboard/leave-type-breakdown")
        if type_breakdown:
            df = pd.DataFrame(type_breakdown)
            palette = [COLORS["primary"], COLORS["secondary"], COLORS["accent"],
                       COLORS["success"], COLORS["warning"], COLORS["danger"], COLORS["primary_light"]]
            fig = go.Figure(go.Pie(
                labels=df["leave_type"], values=df["count"], hole=0.6,
                marker=dict(colors=palette), textinfo="percent",
            ))
            fig.update_layout(
                height=320, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=-0.25),
                font=dict(color=st.session_state.get("chart_text_color", "#64748B")),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No approved leave records yet to chart.")

    # ---- Department breakdown ----
    st.markdown("#### Department-wise Leave Days (Approved)")
    dept_breakdown = api_client.get("/api/dashboard/department-breakdown")
    if dept_breakdown:
        df = pd.DataFrame(dept_breakdown).sort_values("days", ascending=True)
        fig = go.Figure(go.Bar(
            x=df["days"], y=df["department"], orientation="h",
            marker=dict(color=COLORS["secondary"], cornerradius=8),
        ))
        fig.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)"), yaxis=dict(showgrid=False),
            font=dict(color=st.session_state.get("chart_text_color", "#64748B")),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No approved leave records yet to chart.")
