import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ---------- Setup ----------
load_dotenv()
st.set_page_config(page_title="Luna – AI Summarizer", page_icon="🌙", layout="centered")

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
MAX_CHARS = 30000

# Primary model busy-aa irundha ivai order-la try aagum
MODELS = []
for m in [MODEL, "gemini-3.8-flash", "gemini-3.5-flash"]:
    if m not in MODELS:
        MODELS.append(m)

# ---------- Custom CSS + Animations ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Poppins', sans-serif; }

/* Animated gradient background */
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #1a1650, #302b63, #24243e);
    background-size: 400% 400%;
    animation: bgShift 18s ease infinite;
}
@keyframes bgShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Twinkling stars */
.stApp::before {
    content: "";
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background-image:
        radial-gradient(2px 2px at 10% 20%, #fff, transparent),
        radial-gradient(1.5px 1.5px at 30% 70%, #cfc7ff, transparent),
        radial-gradient(2px 2px at 55% 30%, #fff, transparent),
        radial-gradient(1.5px 1.5px at 75% 80%, #cfc7ff, transparent),
        radial-gradient(2px 2px at 90% 15%, #fff, transparent),
        radial-gradient(1px 1px at 20% 90%, #fff, transparent),
        radial-gradient(1.5px 1.5px at 65% 55%, #fff, transparent),
        radial-gradient(1px 1px at 85% 45%, #cfc7ff, transparent);
    animation: twinkle 4s ease-in-out infinite alternate;
}
@keyframes twinkle { from { opacity: .25; } to { opacity: 1; } }

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 780px; position: relative; z-index: 1; }

/* Hero */
.hero { text-align: center; animation: fadeUp .9s ease both; }
.moon { font-size: 72px; display: inline-block; animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 0 25px rgba(167,139,250,.8)); }
@keyframes float { 0%,100% { transform: translateY(0) rotate(-6deg); } 50% { transform: translateY(-14px) rotate(6deg); } }
.title { font-size: 3.2rem; font-weight: 700; margin: 0; letter-spacing: 2px;
         background: linear-gradient(90deg, #a78bfa, #f0abfc, #7dd3fc, #a78bfa);
         background-size: 300% auto; -webkit-background-clip: text; background-clip: text;
         -webkit-text-fill-color: transparent; animation: shine 6s linear infinite; }
@keyframes shine { to { background-position: 300% center; } }
.tagline { color: #cfc7ff; opacity: .85; margin-top: -4px; font-weight: 400; }

@keyframes fadeUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }

/* Glass cards */
.stTabs, .st-key-optionsbox {
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12);
    backdrop-filter: blur(14px);
    border-radius: 20px; padding: 18px 20px;
    animation: fadeUp .9s ease both; animation-delay: .15s;
    box-shadow: 0 10px 40px rgba(0,0,0,.35);
}
.st-key-optionsbox { margin-bottom: 18px; }

/* Labels */
[data-testid="stWidgetLabel"] p { color: #e4defe !important; font-weight: 500; }

/* Tabs */
.stTabs [data-baseweb="tab"] { font-weight: 500; transition: color .3s; }
.stTabs [data-baseweb="tab-highlight"] { background: linear-gradient(90deg, #a78bfa, #f0abfc); height: 3px; }

/* Buttons */
.stButton > button, .stDownloadButton > button {
    width: 100%; border: none; border-radius: 14px; padding: .8rem 1rem;
    font-weight: 600; font-size: 1.05rem; color: #fff;
    background: linear-gradient(90deg, #7c3aed, #c026d3, #7c3aed);
    background-size: 200% auto;
    transition: all .35s ease;
    animation: glow 2.6s ease-in-out infinite;
}
.stButton > button p, .stDownloadButton > button p { color: #fff !important; }
.stButton > button:hover, .stDownloadButton > button:hover {
    background-position: right center; transform: translateY(-3px) scale(1.02);
    box-shadow: 0 12px 30px rgba(192,38,211,.5); color: #fff;
}
.stButton > button:active { transform: scale(.97); }
@keyframes glow {
    0%,100% { box-shadow: 0 0 10px rgba(124,58,237,.5); }
    50% { box-shadow: 0 0 26px rgba(192,38,211,.75); }
}

/* Stat chips */
.chips { display: flex; gap: 10px; margin: 14px 0; animation: fadeUp .5s ease both; }
.chip { flex: 1; text-align: center; padding: 10px; border-radius: 14px;
        background: rgba(167,139,250,.14); border: 1px solid rgba(167,139,250,.3);
        color: #efeaff; font-size: .9rem; transition: transform .3s; }
.chip:hover { transform: translateY(-4px); }
.chip b { display: block; font-size: 1.3rem; color: #f0abfc; }

/* Loader */
.loader { text-align: center; color: #d8ccff; padding: 18px; animation: fadeUp .4s ease both; }
.loader span.dot { display: inline-block; width: 11px; height: 11px; margin: 0 4px; border-radius: 50%;
                   background: linear-gradient(135deg, #a78bfa, #f0abfc); animation: bounce 1.2s infinite ease-in-out; }
.loader span.dot:nth-child(2) { animation-delay: .15s; }
.loader span.dot:nth-child(3) { animation-delay: .3s; }
@keyframes bounce { 0%,80%,100% { transform: scale(.5); opacity: .5; } 40% { transform: scale(1.3); opacity: 1; } }

/* Result card */
.st-key-resultbox {
    margin-top: 18px; padding: 4px 22px;
    background: rgba(255,255,255,.07); border-radius: 20px;
    border: 1px solid rgba(240,171,252,.35);
    box-shadow: 0 0 30px rgba(167,139,250,.2);
    animation: slideIn .7s cubic-bezier(.2,.8,.2,1) both;
}
.st-key-resultbox p, .st-key-resultbox li { color: #f4f1ff !important; line-height: 1.7; }
@keyframes slideIn { from { opacity: 0; transform: translateY(40px) scale(.97); } to { opacity: 1; transform: none; } }

.footer-note { text-align: center; color: #9d93cf; font-size: .8rem; margin-top: 30px; }

/* ===== DARK INPUTS, WHITE TEXT (final override) ===== */
.stApp [data-testid="stTextArea"] div,
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] div,
.stApp [data-testid="stFileUploaderDropzone"] div {
    background: transparent !important;
}

.stApp [data-testid="stTextArea"] div[data-baseweb="textarea"],
.stApp [data-testid="stTextArea"] div[data-baseweb="base-input"],
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
.stApp [data-testid="stFileUploaderDropzone"] {
    background: #1b1740 !important;
    border: 1px solid rgba(167, 139, 250, 0.45) !important;
    border-radius: 14px !important;
    transition: all .3s ease;
}
.stApp [data-testid="stTextArea"] div[data-baseweb="textarea"]:focus-within,
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
.stApp [data-testid="stFileUploaderDropzone"]:hover {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,.25), 0 0 22px rgba(167,139,250,.35);
}

.stApp [data-testid="stTextArea"] textarea,
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] *,
.stApp [data-testid="stFileUploaderDropzone"] *,
.stApp [data-testid="stFileUploaderDropzone"] small {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background: transparent !important;
    caret-color: #f0abfc !important;
}

.stApp [data-testid="stTextArea"] textarea::placeholder {
    color: #9d93cf !important;
    -webkit-text-fill-color: #9d93cf !important;
}

.stApp [data-testid="stSelectbox"] svg,
.stApp [data-testid="stFileUploaderDropzone"] svg { fill: #cfc7ff !important; }

.stApp [data-testid="stFileUploaderDropzone"] button {
    background: rgba(167, 139, 250, 0.25) !important;
    border: 1px solid #a78bfa !important;
    border-radius: 10px !important;
}

/* Tab labels */
.stApp .stTabs [data-baseweb="tab"] p { color: #cfc7ff !important; }
.stApp .stTabs [aria-selected="true"] p { color: #ffffff !important; }

/* Dropdown list popup */
body div[data-baseweb="popover"] ul,
body div[data-baseweb="popover"] li,
body div[data-baseweb="popover"] li * {
    background: #1b1740 !important;
    color: #ffffff !important;
}
body div[data-baseweb="popover"] li:hover,
body div[data-baseweb="popover"] li:hover * {
    background: rgba(167, 139, 250, 0.35) !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ---------- API ----------
def get_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        try:
            key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            key = None
    return key


api_key = get_api_key()
if not api_key:
    st.error("GEMINI_API_KEY not found. Add it to your .env file or Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# ---------- Hero ----------
st.markdown(
    """
<div class="hero">
    <div class="moon">🌙</div>
    <h1 class="title">LUNA</h1>
    <p class="tagline">Long text in, clear summary out.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- Options ----------
length_guide = {
    "Short": "in about 2-3 sentences",
    "Balanced": "in a moderate length, covering the main ideas",
    "Detailed": "in a detailed way, covering main ideas and important supporting points",
}
format_guide = {
    "Paragraph": "Write it as clear, flowing paragraph(s).",
    "Bullet points": "Write it as concise bullet points.",
    "Study notes": "Write it as structured study notes with headings, key terms, and short bullet points.",
}

with st.container(key="optionsbox"):
    col1, col2 = st.columns(2)
    with col1:
        length = st.selectbox("✨ Summary length", list(length_guide.keys()), index=1)
    with col2:
        fmt = st.selectbox("📝 Output format", list(format_guide.keys()))

# ---------- Input ----------
tab_paste, tab_upload = st.tabs(["✍️ Paste text", "📄 Upload file"])

text = ""
with tab_paste:
    pasted = st.text_area("Paste your text here", height=230, placeholder="Drop your long text here...")
    if pasted:
        text = pasted

with tab_upload:
    uploaded = st.file_uploader("Upload a .txt or .md file", type=["txt", "md"])
    if uploaded is not None:
        text = uploaded.read().decode("utf-8", errors="ignore")
        st.success(f"Loaded: {uploaded.name}")

# ---------- Stats chips ----------
if text.strip():
    words = len(text.split())
    chars = len(text)
    read_min = max(1, round(words / 200))
    st.markdown(
        f"""
<div class="chips">
    <div class="chip"><b>{words:,}</b>words</div>
    <div class="chip"><b>{chars:,}</b>characters</div>
    <div class="chip"><b>~{read_min} min</b>read time</div>
</div>
""",
        unsafe_allow_html=True,
    )

LOADER_HTML = """
<div class="loader">
    <span class="dot"></span><span class="dot"></span><span class="dot"></span>
    <div style="margin-top:8px">Luna is reading your text...</div>
</div>
"""


# ---------- Streaming helpers (retry + fallback models) ----------
def is_busy(e):
    msg = str(e)
    return any(c in msg for c in ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED"))


def run_stream(model, prompt, placeholder, loader, fast=True):
    summary = ""
    config = None
    if fast:
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
    for chunk in client.models.generate_content_stream(
        model=model, contents=prompt, config=config
    ):
        if chunk.text:
            if not summary:
                loader.empty()  # hide loader on first words
            summary += chunk.text
            placeholder.markdown(summary + " ▌")  # typing cursor
    placeholder.markdown(summary)
    return summary


def stream_summary(prompt, placeholder, loader):
    last_error = None
    for model in MODELS:
        for attempt in range(3):
            try:
                return run_stream(model, prompt, placeholder, loader, fast=True)
            except Exception as e:
                last_error = e
                if is_busy(e):
                    st.toast(f"Server busy, retrying... ({model})", icon="⏳")
                    time.sleep(2 * (attempt + 1))
                    continue
                # thinking config support illa-nu irundha, adhu illama try
                try:
                    return run_stream(model, prompt, placeholder, loader, fast=False)
                except Exception as e2:
                    last_error = e2
                    if is_busy(e2):
                        time.sleep(2 * (attempt + 1))
                        continue
                    break  # 404 maathiri model problem na next model-ku po
    raise last_error


# ---------- Summarize ----------
st.write("")
if st.button("🌙  Summarize", type="primary"):
    if not text.strip():
        st.warning("Please paste some text or upload a file first.")
    else:
        if len(text) > MAX_CHARS:
            st.warning(f"Text romba perusa irukku, first {MAX_CHARS:,} characters mattum use pannren.")
            text = text[:MAX_CHARS]

        prompt = (
            f"Summarize the following text {length_guide[length]}. "
            f"{format_guide[fmt]} "
            "Do not add information that is not in the text.\n\n"
            f"TEXT:\n{text}"
        )

        loader = st.empty()
        loader.markdown(LOADER_HTML, unsafe_allow_html=True)
        with st.container(key="resultbox"):
            placeholder = st.empty()
            try:
                summary = stream_summary(prompt, placeholder, loader)
                st.session_state["summary"] = summary
            except Exception as e:
                loader.empty()
                st.error(f"Something went wrong: {e}")

# ---------- Download ----------
if st.session_state.get("summary"):
    st.write("")
    st.download_button(
        "⬇️  Download summary",
        data=st.session_state["summary"],
        file_name="luna_summary.txt",
        mime="text/plain",
    )

st.markdown(
    '<p class="footer-note">Avoid submitting confidential information · Powered by Google Gemini</p>',
    unsafe_allow_html=True,
)