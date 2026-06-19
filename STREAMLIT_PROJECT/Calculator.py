import streamlit as st

st.set_page_config(page_title="✨ Beautiful Calculator", page_icon="🧮", layout="centered")

# ---------- SESSION STATE ----------
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = "0"
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- CALLBACKS ----------
def press(val):
    st.session_state.expression += str(val)

def clear_all():
    st.session_state.expression = ""
    st.session_state.result = "0"

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def toggle_sign():
    if st.session_state.expression:
        if st.session_state.expression.startswith("-"):
            st.session_state.expression = st.session_state.expression[1:]
        else:
            st.session_state.expression = "-" + st.session_state.expression

def calculate():
    expr = st.session_state.expression
    if not expr:
        return
    safe_expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-").replace("%", "/100")
    try:
        result = eval(safe_expr, {"__builtins__": {}}, {})
        if isinstance(result, float):
            result = round(result, 10)
            if result == int(result):
                result = int(result)
        st.session_state.history.insert(0, f"{expr} = {result}")
        st.session_state.history = st.session_state.history[:12]
        st.session_state.result = str(result)
        st.session_state.expression = str(result)
    except ZeroDivisionError:
        st.session_state.result = "Cannot divide by 0"
        st.session_state.expression = ""
    except Exception:
        st.session_state.result = "Error"
        st.session_state.expression = ""

def clear_history():
    st.session_state.history = []

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("🎨 Customize")
    color1 = st.color_picker("Gradient start", "#667eea")
    color2 = st.color_picker("Gradient end", "#764ba2")
    st.divider()
    st.header("📜 History")
    if st.session_state.history:
        for h in st.session_state.history:
            st.markdown(f"<div class='hist-item'>{h}</div>", unsafe_allow_html=True)
        st.button("🗑️ Clear history", on_click=clear_history, use_container_width=True)
    else:
        st.caption("No calculations yet.")

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
    max-width: 460px;
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
    color: rgba(255,255,255,0.85);
    margin-bottom: 1.4rem;
    font-size: 0.95rem;
}}
.calc-card {{
    background: rgba(255,255,255,0.18);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 28px;
    padding: 22px 22px 10px 22px;
    border: 1px solid rgba(255,255,255,0.35);
    box-shadow: 0 20px 45px rgba(0,0,0,0.25);
    margin-bottom: 1.2rem;
}}
.display-box {{
    background: rgba(0,0,0,0.18);
    border-radius: 18px;
    padding: 22px 20px;
    margin-bottom: 18px;
    text-align: right;
    min-height: 96px;
}}
.expr-line {{
    color: rgba(255,255,255,0.75);
    font-size: 1.1rem;
    min-height: 24px;
    word-wrap: break-word;
}}
.result-line {{
    color: white;
    font-size: 2.6rem;
    font-weight: 600;
    line-height: 1.1;
    word-wrap: break-word;
}}
div[data-testid="stButton"] > button {{
    width: 100%;
    height: 58px;
    border-radius: 16px !important;
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    margin-bottom: 10px;
    transition: transform 0.08s ease, box-shadow 0.15s ease;
    border: none !important;
}}
div[data-testid="stButton"] > button:active {{
    transform: scale(0.95);
}}
div[data-testid="stButton"] > button[kind="secondary"] {{
    background: rgba(255,255,255,0.85) !important;
    color: #2d2d2d !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.12);
}}
div[data-testid="stButton"] > button[kind="secondary"]:hover {{
    background: rgba(255,255,255,1) !important;
}}
div[data-testid="stButton"] > button[kind="primary"] {{
    background: linear-gradient(135deg, #ff9966 0%, #ff5e62 100%) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(255,94,98,0.45);
}}
div[data-testid="stButton"] > button[kind="primary"]:hover {{
    filter: brightness(1.08);
}}
.hist-item {{
    background: rgba(255,255,255,0.15);
    color: white;
    padding: 8px 10px;
    border-radius: 10px;
    margin-bottom: 6px;
    font-size: 0.85rem;
}}
[data-testid="stSidebar"] {{
    background: rgba(20,20,30,0.55);
    backdrop-filter: blur(10px);
}}
[data-testid="stSidebar"] * {{
    color: white;
}}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1>🧮 Beautiful Calculator</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Simple, elegant, and fully interactive</div>", unsafe_allow_html=True)

# ---------- DISPLAY ----------
st.markdown(f"""
<div class="calc-card">
<div class="display-box">
    <div class="expr-line">{st.session_state.expression if st.session_state.expression else "&nbsp;"}</div>
    <div class="result-line">{st.session_state.result}</div>
</div>
""", unsafe_allow_html=True)

# ---------- BUTTON GRID ----------
rows = [
    [("C", "secondary", clear_all, None), ("⌫", "secondary", backspace, None),
     ("±", "secondary", toggle_sign, None), ("÷", "primary", press, ("÷",))],
    [("7", "secondary", press, ("7",)), ("8", "secondary", press, ("8",)),
     ("9", "secondary", press, ("9",)), ("×", "primary", press, ("×",))],
    [("4", "secondary", press, ("4",)), ("5", "secondary", press, ("5",)),
     ("6", "secondary", press, ("6",)), ("−", "primary", press, ("−",))],
    [("1", "secondary", press, ("1",)), ("2", "secondary", press, ("2",)),
     ("3", "secondary", press, ("3",)), ("+", "primary", press, ("+",))],
]

for row in rows:
    cols = st.columns(4)
    for (label, kind, fn, args), c in zip(row, cols):
        c.button(label, type=kind, on_click=fn, args=args, use_container_width=True)

last_cols = st.columns([2, 1, 1])
last_cols[0].button("0", type="secondary", on_click=press, args=("0",), use_container_width=True)
last_cols[1].button(".", type="secondary", on_click=press, args=(".",), use_container_width=True)
last_cols[2].button("=", type="primary", on_click=calculate, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<div style='text-align:center;color:rgba(255,255,255,0.7);font-size:0.8rem;'>"
    "Built with Streamlit ✨ — type using the buttons above</div>",
    unsafe_allow_html=True,
)