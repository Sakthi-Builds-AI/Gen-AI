"""
pages/landing.py
------------------
The pre-login marketing page: hero, stats, features, testimonials,
pricing, footer. Pure presentation -- no API calls needed.
"""

import streamlit as st
from styles import COLORS


def render(go_to_login):
    st.markdown("""
        <div class="hero-wrap">
            <div class="hero-title">Transform Workforce<br>Leave Management</div>
            <div class="hero-sub">
                Streamline employee leave requests, approvals, workforce planning,
                and HR operations with one intelligent platform.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Get Started →", use_container_width=True):
                go_to_login()
        with c2:
            st.button("Request Demo", use_container_width=True, disabled=True,
                       help="Demo scheduling isn't wired up in this build -- use Get Started to explore live with seeded data.")
        with c3:
            if st.button("Sign In", use_container_width=True):
                go_to_login()

    st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)

    # ---- Stats strip ----
    stats = [
        ("18+", "Departments supported per org"),
        ("8", "Configurable leave types"),
        ("99.9%", "Platform uptime target"),
        ("4", "Role-based access levels"),
    ]
    cols = st.columns(4)
    for col, (num, label) in zip(cols, stats):
        with col:
            st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:1.8rem; font-weight:800; color:var(--primary);">{num}</div>
                    <div style="font-size:0.82rem; color:var(--text-muted); margin-top:4px;">{label}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)

    # ---- Features ----
    st.markdown("### Built for how HR teams actually work")
    features = [
        ("📊", "Executive Dashboard", "Live KPIs, monthly trends, and department-wise leave analytics in one view."),
        ("🧑‍💼", "Self-Service Portal", "Employees apply for leave, track balances, and see history without filing a ticket."),
        ("✅", "Approval Center", "Managers see team availability and approve, reject, or ask for clarification in seconds."),
        ("🏢", "HR Administration", "Manage employees, departments, leave policy, and the holiday calendar from one place."),
        ("📈", "Reports & Analytics", "Export leave summaries, attendance analysis, and department reports to Excel or CSV."),
        ("🔔", "Notification Center", "Stay on top of pending approvals and upcoming leave expiry at a glance."),
    ]
    feat_cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with feat_cols[i % 3]:
            st.markdown(f"""
                <div class="glass-card" style="margin-bottom:16px; min-height:170px;">
                    <div style="font-size:1.6rem;">{icon}</div>
                    <div style="font-weight:700; margin:8px 0 6px 0;">{title}</div>
                    <div style="font-size:0.86rem; color:var(--text-muted); line-height:1.5;">{desc}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    # ---- Testimonials ----
    st.markdown("### What teams say")
    quotes = [
        ("\"We replaced three spreadsheets and a shared inbox with this in a week.\"", "— Head of People Ops, mid-size SaaS company"),
        ("\"Approval time dropped from days to hours once managers could see team availability.\"", "— Engineering Director"),
        ("\"The dashboard alone justified the rollout -- finally one source of truth for leave.\"", "— HR Business Partner"),
    ]
    q_cols = st.columns(3)
    for col, (quote, author) in zip(q_cols, quotes):
        with col:
            st.markdown(f"""
                <div class="glass-card" style="min-height:140px;">
                    <div style="font-style:italic; font-size:0.88rem; line-height:1.5;">{quote}</div>
                    <div style="margin-top:10px; font-size:0.8rem; color:var(--text-muted); font-weight:600;">{author}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align:center; padding:20px; color:var(--text-muted); font-size:0.82rem; border-top:1px solid var(--surface-border);">
            © 2026 PUREWORKS · Simple AI powered solutions
        </div>
    """, unsafe_allow_html=True)
