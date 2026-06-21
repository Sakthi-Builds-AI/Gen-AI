"""
app.py
------
Main Streamlit entrypoint for the Leave Management Portal.

Run with:  cd frontend && streamlit run app.py
(Make sure the backend is already running on port 8000 -- see README.)
"""

import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app_pages"))

from styles import inject_css
import api_client

from app_pages import landing, auth_page, dashboard_page, employee_portal_page, \
    manager_approvals_page, hr_admin_page, reports_page
st.set_page_config(
    page_title="PURE WORKS",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="auto",
)

# ---------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------
defaults = {
    "page": "landing",
    "access_token": None,
    "role": None,
    "full_name": None,
    "employee_id": None,
    "dark_mode": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

inject_css(dark_mode=st.session_state.dark_mode)
st.session_state["chart_text_color"] = "#CBD5E1" if st.session_state.dark_mode else "#64748B"

is_logged_in = st.session_state.access_token is not None

# ---------------------------------------------------------------------
# Pre-login: landing page or login page (no chrome)
# ---------------------------------------------------------------------
if not is_logged_in:
    if st.session_state.page == "login":
        auth_page.render()
    else:
         # Lightweight top bar even on the marketing page
        c1, c2, c3 = st.columns([1, 3, 1])
        with c2:
            st.markdown("""
                <div style="text-align:center; padding-top:6px;">
                    <div class="hero-title" style="margin-bottom:6px;">🗓️ PUREWORKS</div>
                    <div style="color:var(--text-muted); font-size:1.32rem; margin-top:1px;">Simple AI powered solutions</div>
                </div>
            """, unsafe_allow_html=True)
       
        landing.render(go_to_login=lambda: (st.session_state.update(page="login"), st.rerun()))
    st.stop()

# ---------------------------------------------------------------------
# Logged-in shell: top nav + sidebar + routed page content
# ---------------------------------------------------------------------
ROLE = st.session_state.role

# Build the nav menu available to this role
nav_items = [("dashboard", "🏠 Dashboard")]
if ROLE in ("Employee", "Manager"):
    nav_items.append(("employee_portal", "👤 Employee Portal"))
if ROLE in ("Manager", "HR Admin", "Super Admin"):
    nav_items.append(("approvals", "✅ Approvals"))
if ROLE in ("HR Admin", "Super Admin"):
    nav_items.append(("hr_admin", "🏢 HR Administration"))
if ROLE in ("Manager", "HR Admin", "Super Admin"):
    nav_items.append(("reports", "📊 Reports"))
nav_items.append(("settings", "⚙️ Settings"))

if st.session_state.page not in [k for k, _ in nav_items]:
    st.session_state.page = "dashboard"

# ---- Top nav bar ----
top_left, top_right = st.columns([3, 2])
with top_left:
     st.markdown(f"""
        <div class="topnav" style="justify-content:center;">
            <div class="topnav-brand" style="text-align:center;">
                <div>🗓️ PUREWORKS</div>
                <div class="topnav-tagline" style="margin-top:2px;">Simple AI powered solutions</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
with top_right:
    nc1, nc2, nc3 = st.columns([2, 1, 1])
    with nc1:
        st.markdown(f"""
            <div style="text-align:right; padding-top:18px; font-size:0.85rem;">
                <strong>{st.session_state.full_name}</strong><br>
                <span style="color:var(--text-muted);">{ROLE}</span>
            </div>
        """, unsafe_allow_html=True)
    with nc2:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️", help="Toggle dark / light mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    with nc3:
        unread = api_client.get("/api/notifications/unread-count")
        unread_count = unread["unread_count"] if unread else 0
        bell_label = f"🔔 {unread_count}" if unread_count else "🔔"
        with st.popover(bell_label):
            st.markdown("**Notifications**")
            notes = api_client.get("/api/notifications")
            if notes:
                if unread_count and st.button("Mark all as read", key="mark_all_read", use_container_width=True):
                    api_client.post("/api/notifications/mark-all-read")
                    st.rerun()
                for n in notes:
                    dot = "🔵" if not n["is_read"] else "⚪"
                    st.caption(f"{dot} {n['message']}")
            else:
                st.caption("No notifications yet.")

# ---- Sidebar ----
with st.sidebar:
    st.markdown("#### Navigation")
    for key, label in nav_items:
        is_active = st.session_state.page == key
        if st.button(label, use_container_width=True, type="primary" if is_active else "secondary", key=f"nav_{key}"):
            st.session_state.page = key
            st.rerun()
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        for key in defaults:
            st.session_state[key] = defaults[key]
        st.session_state.page = "landing"
        st.rerun()

# ---- Routed page content ----
page = st.session_state.page
if page == "dashboard":
    dashboard_page.render()
elif page == "employee_portal":
    employee_portal_page.render()
elif page == "approvals":
    manager_approvals_page.render()
elif page == "hr_admin":
    hr_admin_page.render()
elif page == "reports":
    reports_page.render()
elif page == "settings":
    st.markdown("### ⚙️ Settings")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"**Name:** {st.session_state.full_name}")
    st.markdown(f"**Role:** {ROLE}")
    st.markdown(f"**Employee ID:** {st.session_state.employee_id or '—'}")
    st.markdown("**Theme:** use the 🌙/☀️ toggle in the top right.")
    st.caption("Audit logs and notification preferences are planned for a future phase.")
    st.markdown('</div>', unsafe_allow_html=True)
