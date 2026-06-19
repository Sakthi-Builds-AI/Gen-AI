import streamlit as st

st.set_page_config(page_title="🎓 Student Grade Calculator", page_icon="🎓", layout="centered")

# ---------- GRADE SCALE (universal percentage bands) ----------
GRADE_ORDER = ["A", "B", "C", "D", "F"]

BAND_LABEL = "90-100: A   80-89: B   70-79: C   60-69: D   Below 60: F"

def mark_to_grade(mark):
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "F"

def grade_color(letter):
    if letter == "A":
        return "#29c060"
    if letter == "B":
        return "#3b82f6"
    if letter == "C":
        return "#f59e0b"
    if letter == "D":
        return "#67310a"
    return "#ef4444"

def remark(letter):
    if letter == "A":
        return "Outstanding! Top of the class. 🌟"
    if letter == "B":
        return "Great work — well above average. 👍"
    if letter == "C":
        return "Decent effort — aim a bit higher next time. 📈"
    if letter == "D":
        return "Just passing — extra practice will help. 💪"
    return "Failing — needs serious improvement and support. 🆘"

# ---------- SESSION STATE ----------
if "subjects" not in st.session_state:
    st.session_state.subjects = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 0

def add_subject():
    sid = st.session_state.next_id
    st.session_state.subjects.append(sid)
    st.session_state[f"name_{sid}"] = f"Subject {len(st.session_state.subjects)}"
    st.session_state[f"mark_{sid}"] = 100
    st.session_state.next_id += 1

def remove_subject(sid):
    if sid in st.session_state.subjects:
        st.session_state.subjects.remove(sid)
    st.session_state.pop(f"name_{sid}", None)
    st.session_state.pop(f"mark_{sid}", None)

def clear_all():
    for sid in list(st.session_state.subjects):
        remove_subject(sid)

# seed with 3 subjects on first load
if not st.session_state.subjects and st.session_state.next_id == 0:
    for _ in range(5):
        add_subject()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("🎨 Customize")
    color1 = st.color_picker("Gradient start", "#44817c")
    color2 = st.color_picker("Gradient end", "#3f6d86")
    st.divider()
    st.button("🗑️ Clear all subjects", on_click=clear_all, use_container_width=True)
    st.divider()
    with st.expander("ℹ️ How is the grade calculated?"):
        st.write(
            "Enter each subject's mark as a percentage (0-100). Every "
            "subject is graded using the standard band below, the overall "
            "percentage is the simple average of all subject marks (no "
            "credit weighting), and that average is graded using the same "
            "band."
        )
        st.markdown("**90 - 100** → Grade A")
        st.markdown("**80 - 89** → Grade B")
        st.markdown("**70 - 79** → Grade C")
        st.markdown("**60 - 69** → Grade D")
        st.markdown("**Below 60** → Grade F (Fail)")

# ---------- CSS ----------
# NOTE: no blank lines allowed inside the <style> block below — Streamlit's
# markdown parser can terminate the raw-HTML block early at a blank line and
# render the remaining CSS as literal visible text on the page.
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {{
    font-family: 'Poppins', sans-serif;
}}
.stApp {{
    background: linear-gradient(135deg, {color1} 0%, {color2} 100%);
    background-attachment: fixed;
}}
.block-container {{
    max-width: 600px;
    padding-top: 2rem;
}}
h1 {{
    color: white;
    text-align: center;
    font-weight: 700;
    text-shadow: 0 2px 12px rgba(0,0,0,0.25);
    margin-bottom: 0.2rem;
}}
.subtitle {{
    text-align: center;
    color: rgba(255,255,255,0.9);
    margin-bottom: 1.4rem;
    font-size: 0.95rem;
}}
.card {{
    background: rgba(255,255,255,0.18);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 24px;
    padding: 22px;
    border: 1px solid rgba(255,255,255,0.35);
    box-shadow: 0 20px 45px rgba(0,0,0,0.2);
    margin-bottom: 1.2rem;
}}
.row-label {{
    color: rgba(255,255,255,0.85);
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 4px;
}}
div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {{
    border-radius: 12px !important;
    background: rgba(255,255,255,0.9) !important;
}}
div[data-testid="stButton"] > button {{
    border-radius: 12px !important;
    font-weight: 600 !important;
    border: none !important;
}}
div[data-testid="stButton"] > button[kind="secondary"] {{
    background: rgba(255,255,255,0.85) !important;
    color: #2d2d2d !important;
}}
div[data-testid="stButton"] > button[kind="primary"] {{
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(17,153,142,0.45);
}}
.remove-btn button {{
    background: rgba(239,68,68,0.85) !important;
    color: white !important;
}}
.empty-state {{
    text-align: center;
    color: rgba(255,255,255,0.85);
    padding: 30px 10px;
}}
.stat-box {{
    background: rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 14px 10px;
    text-align: center;
}}
.stat-num {{
    font-size: 1.6rem;
    font-weight: 700;
    color: white;
}}
.stat-label {{
    font-size: 0.75rem;
    color: rgba(255,255,255,0.8);
    text-transform: uppercase;
    letter-spacing: 0.03em;
}}
.overall-grade {{
    font-size: 3.2rem;
    font-weight: 700;
    text-align: center;
    line-height: 1.1;
}}
.overall-pct {{
    text-align: center;
    color: rgba(255,255,255,0.9);
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: -6px;
}}
.remark-text {{
    text-align: center;
    color: rgba(255,255,255,0.95);
    font-size: 0.95rem;
    margin-top: 4px;
    margin-bottom: 10px;
}}
.bar-row {{
    display: flex;
    align-items: center;
    margin-bottom: 8px;
    color: white;
    font-size: 0.85rem;
}}
.bar-label {{
    width: 28px;
    font-weight: 700;
}}
.bar-track {{
    flex: 1;
    background: rgba(255,255,255,0.2);
    border-radius: 8px;
    height: 16px;
    margin: 0 8px;
    overflow: hidden;
}}
.bar-fill {{
    height: 100%;
    border-radius: 8px;
}}
.bar-count {{
    width: 60px;
    text-align: right;
    color: rgba(255,255,255,0.85);
}}
.best-weak-line {{
    color: white;
    font-size: 0.95rem;
    margin-bottom: 6px;
}}
.row-badge {{
    font-weight: 700;
    text-align: center;
    padding-top: 10px;
}}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1>🎓 Student Grade Calculator</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Add your subjects, enter each mark as a percentage, and see your overall grade</div>",
    unsafe_allow_html=True,
)

# ---------- SUBJECTS CARD ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)

if not st.session_state.subjects:
    st.markdown(
        "<div class='empty-state'>No subjects yet.<br>Click <b>+ Add Subject</b> below to get started.</div>",
        unsafe_allow_html=True,
    )
else:
    header_cols = st.columns([3, 2, 1, 1])
    header_cols[0].markdown("<div class='row-label'>Subject</div>", unsafe_allow_html=True)
    header_cols[1].markdown("<div class='row-label'>Mark (%)</div>", unsafe_allow_html=True)
    header_cols[2].markdown("<div class='row-label'>Grade</div>", unsafe_allow_html=True)
    header_cols[3].markdown("<div class='row-label'>&nbsp;</div>", unsafe_allow_html=True)

    for sid in st.session_state.subjects:
        c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
        c1.text_input(
            "Subject name", key=f"name_{sid}", label_visibility="collapsed",
            placeholder="Subject name",
        )
        c2.number_input(
            "Mark", key=f"mark_{sid}", label_visibility="collapsed",
            min_value=0, max_value=100, step=1,
        )
        row_grade = mark_to_grade(st.session_state[f"mark_{sid}"])
        c3.markdown(
            f"<div class='row-badge' style='color:{grade_color(row_grade)};'>{row_grade}</div>",
            unsafe_allow_html=True,
        )
        with c4:
            st.markdown("<div class='remove-btn'>", unsafe_allow_html=True)
            st.button("🗑️", key=f"remove_{sid}", on_click=remove_subject, args=(sid,), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

st.button("➕ Add Subject", on_click=add_subject, type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------- RESULTS ----------
if st.session_state.subjects:
    entries = []
    for i, sid in enumerate(st.session_state.subjects, start=1):
        name = st.session_state.get(f"name_{sid}", "").strip() or f"Subject {i}"
        mark = st.session_state.get(f"mark_{sid}", 75)
        entries.append((name, mark, mark_to_grade(mark)))

    total = len(entries)
    avg_mark = sum(e[1] for e in entries) / total
    overall_letter = mark_to_grade(avg_mark)
    overall_color = grade_color(overall_letter)

    passed = sum(1 for e in entries if e[2] != "F")
    failed = total - passed

    best = max(entries, key=lambda e: e[1])
    weakest = min(entries, key=lambda e: e[1])

    counts = {g: 0 for g in GRADE_ORDER}
    for _, _, g in entries:
        counts[g] += 1
    max_count = max(counts.values()) if counts else 1

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='overall-grade' style='color:{overall_color};'>{overall_letter}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div class='overall-pct'>{avg_mark:.1f}% average</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='remark-text'>{remark(overall_letter)}</div>", unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    s1.markdown(f"<div class='stat-box'><div class='stat-num'>{total}</div><div class='stat-label'>Subjects</div></div>", unsafe_allow_html=True)
    s2.markdown(f"<div class='stat-box'><div class='stat-num'>{passed}</div><div class='stat-label'>Passed</div></div>", unsafe_allow_html=True)
    s3.markdown(f"<div class='stat-box'><div class='stat-num'>{failed}</div><div class='stat-label'>Failed</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='best-weak-line'>🏆 <b>Best:</b> {best[0]} — {best[1]}% "
        f"(<span style='color:{grade_color(best[2])}; font-weight:700;'>{best[2]}</span>)</div>",
        unsafe_allow_html=True,
    )
    if weakest[0] != best[0]:
        st.markdown(
            f"<div class='best-weak-line'>📉 <b>Weakest:</b> {weakest[0]} — {weakest[1]}% "
            f"(<span style='color:{grade_color(weakest[2])}; font-weight:700;'>{weakest[2]}</span>)</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='row-label'>Grade Distribution</div>", unsafe_allow_html=True)
    bars_html = ""
    for g in GRADE_ORDER:
        c = counts[g]
        if c == 0:
            continue
        width_pct = int((c / max_count) * 100)
        bars_html += (
            f"<div class='bar-row'>"
            f"<div class='bar-label' style='color:{grade_color(g)};'>{g}</div>"
            f"<div class='bar-track'><div class='bar-fill' style='width:{width_pct}%; "
            f"background:{grade_color(g)};'></div></div>"
            f"<div class='bar-count'>{c} subj.</div>"
            f"</div>"
        )
    st.markdown(bars_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<div style='text-align:center;color:rgba(255,255,255,0.75);font-size:0.8rem;'>"
    "Built with Streamlit ✨</div>",
    unsafe_allow_html=True,
)