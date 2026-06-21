"""
styles.py
---------
Central place for the portal's visual identity: the corporate color
tokens from the brief, plus the CSS that gives Streamlit's default
chrome a glassmorphic, enterprise-SaaS look in both light and dark mode.

Streamlit doesn't expose real theme variables to inject into arbitrary
CSS, so we hand-roll CSS custom properties and toggle a `data-theme`
attribute on the root container based on session state.
"""

import streamlit as st

# ---- Brand tokens (from the design brief) --------------------------------
COLORS = {
    "primary": "#2563EB",
    "primary_light": "#3B82F6",
    "secondary": "#14B8A6",
    "accent": "#8B5CF6",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "bg_light": "#F8FAFC",
    "text_light": "#0F172A",
}


def inject_css(dark_mode: bool = False):
    if dark_mode:
        bg = "#0B1220"
        surface = "rgba(255, 255, 255, 0.06)"
        surface_border = "rgba(255, 255, 255, 0.10)"
        text = "#F1F5F9"
        text_muted = "#94A3B8"
        card_shadow = "0 8px 32px rgba(0, 0, 0, 0.45)"
    else:
        bg = COLORS["bg_light"]
        surface = "rgba(255, 255, 255, 0.65)"
        surface_border = "rgba(15, 23, 42, 0.06)"
        text = COLORS["text_light"]
        text_muted = "#64748B"
        card_shadow = "0 8px 32px rgba(15, 23, 42, 0.08)"

    st.markdown(f"""
    <style>
        :root {{
            --primary: {COLORS['primary']};
            --primary-light: {COLORS['primary_light']};
            --secondary: {COLORS['secondary']};
            --accent: {COLORS['accent']};
            --success: {COLORS['success']};
            --warning: {COLORS['warning']};
            --danger: {COLORS['danger']};
            --bg: {bg};
            --surface: {surface};
            --surface-border: {surface_border};
            --text: {text};
            --text-muted: {text_muted};
            --card-shadow: {card_shadow};
        }}

        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, sans-serif;
        }}

        .stApp {{
            background: var(--bg);
            color: var(--text);
        }}

        h1, h2, h3, .hero-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}

        /* ---- Glass card ---- */
        .glass-card {{
            background: var(--surface);
            backdrop-filter: blur(16px) saturate(180%);
            -webkit-backdrop-filter: blur(16px) saturate(180%);
            border: 1px solid var(--surface-border);
            border-radius: 18px;
            padding: 22px 24px;
            box-shadow: var(--card-shadow);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }}
        .glass-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 14px 40px rgba(37, 99, 235, 0.18);
        }}

        /* ---- KPI card ---- */
        .kpi-card {{
            background: var(--surface);
            backdrop-filter: blur(16px) saturate(180%);
            -webkit-backdrop-filter: blur(16px) saturate(180%);
            border: 1px solid var(--surface-border);
            border-left: 4px solid var(--accent-color, var(--primary));
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: var(--card-shadow);
            transition: transform 0.2s ease;
        }}
        .kpi-card:hover {{ transform: translateY(-2px); }}
        .kpi-label {{
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 6px;
        }}
        .kpi-value {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            color: var(--text);
            line-height: 1.1;
        }}
        .kpi-icon {{ font-size: 1.6rem; margin-bottom: 6px; }}

        /* ---- Pills / badges ---- */
        .badge {{
            display: inline-block;
            padding: 3px 12px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .badge-success {{ background: rgba(34,197,94,0.15); color: var(--success); }}
        .badge-warning {{ background: rgba(245,158,11,0.15); color: var(--warning); }}
        .badge-danger  {{ background: rgba(239,68,68,0.15);  color: var(--danger); }}
        .badge-info    {{ background: rgba(37,99,235,0.15);  color: var(--primary); }}

        /* ---- Top nav ---- */
        .topnav {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 24px;
            background: var(--surface);
            backdrop-filter: blur(16px);
            border: 1px solid var(--surface-border);
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: var(--card-shadow);
        }}
        .topnav-brand {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
            font-size: 1.15rem;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .topnav-tagline {{
            font-size: 0.78rem;
            color: var(--text-muted);
            font-weight: 500;
        }}

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {{
            background: var(--bg);
            border-right: 1px solid var(--surface-border);
        }}

        /* ---- Buttons ---- */
        ./* Lighter pill-style button for secondary actions like "Sign In" --
           kept visually quiet so it doesn't compete with primary CTAs */
        .stButton > button[kind="secondary"] {{
            background: var(--surface);
            color: var(--primary);
            border: 1.5px solid var(--primary);
            box-shadow: none;
            border-radius: 999px;
            font-weight: 600;
            padding: 4px 22px;
        }}
        .stButton > button[kind="secondary"]:hover {{
            background: rgba(37, 99, 235, 0.08);
            transform: translateY(-1px);
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.15);
        }}

        /* ---- Progress bars ---- */
        .balance-track {{
            background: var(--surface-border);
            border-radius: 999px;
            height: 10px;
            width: 100%;
            overflow: hidden;
            margin-top: 6px;
        }}
        .balance-fill {{
            height: 100%;
            border-radius: 999px;
            transition: width 0.4s ease;
        }}

        /* ---- Hero (landing page) ---- */
        .hero-wrap {{
            text-align: center;
            padding: 70px 20px 50px 20px;
        }}
        .hero-title {{
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--accent) 60%, var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.15;
            margin-bottom: 14px;
        }}
        .hero-sub {{
            font-size: 1.1rem;
            color: var(--text-muted);
            max-width: 640px;
            margin: 0 auto 28px auto;
            line-height: 1.6;
        }}

        /* Hide default Streamlit chrome that clashes with the custom design */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{ background: transparent; }}
    </style>
    """, unsafe_allow_html=True)


def kpi_card(icon: str, label: str, value, accent_color: str = COLORS["primary"]):
    st.markdown(f"""
        <div class="kpi-card" style="--accent-color: {accent_color};">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


def balance_bar(label: str, used: int, total: int, color: str):
    remaining = max(total - used, 0)
    pct = int((remaining / total) * 100) if total else 0
    st.markdown(f"""
        <div style="margin-bottom: 14px;">
            <div style="display:flex; justify-content:space-between; font-size:0.85rem; font-weight:600;">
                <span>{label}</span>
                <span style="color:var(--text-muted);">{remaining} / {total} days left</span>
            </div>
            <div class="balance-track">
                <div class="balance-fill" style="width:{pct}%; background:{color};"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def badge(text: str, kind: str = "info") -> str:
    return f'<span class="badge badge-{kind}">{text}</span>'
