"""
pages/auth_page.py
--------------------
Login screen. Posts to /api/auth/login and stashes the JWT + role info
into st.session_state on success.
"""

import streamlit as st
import api_client


def render():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
            <div style="text-align:center; margin-bottom:10px;">
                <div style="font-size:1.8rem;">🗓️</div>
                <div style="font-weight:800; font-size:1.3rem;">Welcome back</div>
                <div style="color:var(--text-muted); font-size:0.85rem;">Sign in to PUREWORKS</div>
            </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="e.g. rahul.dev")
            password = st.text_input("Password", type="password", placeholder="••••••••")

            if st.button("Sign In", use_container_width=True):
                if not username or not password:
                    st.warning("Enter both username and password.")
                else:
                    data = api_client.post("/api/auth/login", {"username": username, "password": password})
                    if data:
                        st.session_state.access_token = data["access_token"]
                        st.session_state.role = data["role"]
                        st.session_state.full_name = data["full_name"]
                        st.session_state.employee_id = data["employee_id"]
                        st.session_state.page = "dashboard"
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("Demo credentials"):
            st.markdown("""
            All demo accounts use password: **Demo@123**

            | Username | Role |
            |---|---|
            | `superadmin` | Super Admin |
            | `priya.hr` | HR Admin |
            | `arjun.mgr` | Manager (Engineering) |
            | `rahul.dev` | Employee |
            """)

        if st.button("← Back to home"):
            st.session_state.page = "landing"
            st.rerun()
