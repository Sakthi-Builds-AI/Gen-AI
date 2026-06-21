"""
pages/manager_approvals_page.py
----------------------------------
Manager Approval Center: view team requests, see team availability,
and approve / reject / request clarification with a comment.
"""

import streamlit as st
from datetime import date, timedelta

import api_client
from styles import badge, COLORS

STATUS_BADGE = {"Approved": "success", "Pending": "warning", "Rejected": "danger",
                "Clarification Requested": "info"}


def render():
    st.markdown("### ✅ Manager Approval Center")

    filter_choice = st.radio("Filter", ["Pending", "All"], horizontal=True, label_visibility="collapsed")
    status_filter = "Pending" if filter_choice == "Pending" else None

    requests_list = api_client.get("/api/leaves/team", params={"status_filter": status_filter} if status_filter else None)

    if not requests_list:
        st.info("Nothing to review here right now.")
    else:
        for r in requests_list:
            with st.container():
                st.markdown('<div class="glass-card" style="margin-bottom:14px;">', unsafe_allow_html=True)
                top = st.columns([3, 1])
                with top[0]:
                    st.markdown(f"**{r['employee_name']}** · {r['department']}")
                    st.markdown(
                        f"{r['leave_type']} &nbsp;·&nbsp; {r['start_date']} → {r['end_date']} "
                        f"&nbsp;·&nbsp; {r['days_requested']} day(s)",
                        unsafe_allow_html=True,
                    )
                    st.caption(r["reason"] or "No reason provided")
                with top[1]:
                    st.markdown(badge(r["status"], STATUS_BADGE.get(r["status"], "info")), unsafe_allow_html=True)

                # ---- Team availability snippet for this date range ----
                avail = api_client.get(
                    "/api/leaves/team-availability",
                    params={"start_date": r["start_date"], "end_date": r["end_date"], "department": r["department"]},
                )
                others_off = [a for a in avail if a["employee_id"] != r["employee_id"]]
                if others_off:
                    names = ", ".join(a["employee_name"] for a in others_off)
                    st.caption(f"⚠️ Also off in this window: {names}")

                if r["status"] == "Pending":
                    comment = st.text_input("Comment (optional)", key=f"comment_{r['leave_id']}",
                                             placeholder="Add a note visible to the employee")
                    b1, b2, b3 = st.columns(3)
                    with b1:
                        if st.button("✅ Approve", key=f"approve_{r['leave_id']}", use_container_width=True):
                            api_client.post(f"/api/leaves/{r['leave_id']}/decision",
                                             {"status": "Approved", "manager_comments": comment or "Approved"})
                            st.success("Approved.")
                            st.rerun()
                    with b2:
                        if st.button("❌ Reject", key=f"reject_{r['leave_id']}", use_container_width=True):
                            api_client.post(f"/api/leaves/{r['leave_id']}/decision",
                                             {"status": "Rejected", "manager_comments": comment or "Rejected"})
                            st.warning("Rejected.")
                            st.rerun()
                    with b3:
                        if st.button("💬 Ask for clarification", key=f"clarify_{r['leave_id']}", use_container_width=True):
                            if not comment:
                                st.warning("Add a comment describing what you need clarified.")
                            else:
                                api_client.post(f"/api/leaves/{r['leave_id']}/decision",
                                                 {"status": "Clarification Requested", "manager_comments": comment})
                                st.info("Clarification requested.")
                                st.rerun()
                elif r.get("manager_comments"):
                    st.caption(f"Your note: {r['manager_comments']}")

                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("#### Team Availability — Next 14 Days")
    today = date.today()
    avail = api_client.get(
        "/api/leaves/team-availability",
        params={"start_date": str(today), "end_date": str(today + timedelta(days=14))},
    )
    my_team = api_client.get("/api/leaves/team")
    my_team_ids = {r["employee_id"] for r in my_team} if my_team else set()
    team_avail = [a for a in avail if a["employee_id"] in my_team_ids] if avail else []

    if not team_avail:
        st.info("No one on your team has approved leave in the next 14 days.")
    else:
        for a in team_avail:
            st.markdown(
                f"<div class='glass-card' style='margin-bottom:8px; padding:12px 16px;'>"
                f"🌴 <strong>{a['employee_name']}</strong> — {a['leave_type']} "
                f"({a['start_date']} → {a['end_date']})</div>",
                unsafe_allow_html=True,
            )
