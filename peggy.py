import streamlit as st
import anthropic
from datetime import date

st.set_page_config(
    page_title="PEGGY — MindxBridge",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, sans-serif !important;
}
.stApp {
    background: linear-gradient(160deg, #060D18 0%, #0D2137 60%);
}
#MainMenu, footer, header { visibility: hidden; }

section[data-testid="stSidebar"] {
    background: #060D18 !important;
    border-right: 1px solid rgba(30,144,255,0.15);
}

.main .block-container { padding-top: 2rem; max-width: 900px; }

h1, h2, h3 { color: #FFFFFF !important; font-family: 'Inter', sans-serif !important; }

.top-line {
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, #1E90FF, transparent);
    margin-bottom: 1.5rem;
}

.peggy-header {
    margin-bottom: 2rem;
}
.peggy-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -1px;
    margin: 0;
    line-height: 1;
}
.peggy-title span { color: #1E90FF; }
.peggy-sub {
    color: #687C94;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 0.4rem;
    letter-spacing: 1px;
}

.stTextArea > div > textarea {
    background: rgba(6,13,24,0.9) !important;
    color: #E4ECF5 !important;
    border: 1px solid rgba(30,144,255,0.25) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
}
.stTextArea > div > textarea:focus {
    border-color: #1E90FF !important;
    box-shadow: 0 0 0 2px rgba(30,144,255,0.15) !important;
}
.stTextInput > div > input {
    background: rgba(6,13,24,0.9) !important;
    color: #E4ECF5 !important;
    border: 1px solid rgba(30,144,255,0.25) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
}

.stButton > button {
    background: #1E90FF !important;
    color: #060D18 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    letter-spacing: 0.3px;
}
.stButton > button:hover {
    background: #4aaeff !important;
    transform: translateY(-1px);
}

.stRadio > div {
    background: rgba(6,13,24,0.6);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    border: 1px solid rgba(30,144,255,0.15);
}

.response-box {
    background: rgba(6,13,24,0.7);
    border-left: 3px solid #1E90FF;
    border-radius: 0 10px 10px 0;
    padding: 1.5rem 1.75rem;
    margin: 1.25rem 0;
    color: #E4ECF5;
    line-height: 1.75;
    font-size: 0.95rem;
    white-space: pre-wrap;
}

.approval-bar {
    display: flex;
    gap: 0.75rem;
    align-items: center;
    margin: 0.75rem 0 1.5rem 0;
}

.chip {
    display: inline-block;
    background: rgba(30,144,255,0.12);
    color: #1E90FF;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    border: 1px solid rgba(30,144,255,0.3);
    border-radius: 5px;
    padding: 2px 7px;
}

.card {
    background: rgba(6,13,24,0.6);
    border: 1px solid rgba(30,144,255,0.15);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}

.idle-quote {
    background: rgba(6,13,24,0.5);
    border: 1px solid rgba(30,144,255,0.12);
    border-radius: 10px;
    padding: 1.5rem;
    margin-top: 1rem;
    text-align: center;
}

.status-done    { color: #4CAF50; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; }
.status-wait    { color: #FFB347; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; }
.status-active  { color: #1E90FF; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; }
.status-idle    { color: #687C94; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; }
.flag           { color: #FFB347; font-size: 0.82rem; padding: 3px 0; }
.sidebar-label  { color: #687C94; font-size: 0.72rem; font-family: 'JetBrains Mono', monospace; letter-spacing: 1px; text-transform: uppercase; }
.muted          { color: #B0BECE; }
.faint          { color: #687C94; }
.accent         { color: #1E90FF; }

hr { border: none; border-top: 1px solid rgba(30,144,255,0.12); margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

BRAND_SYSTEM = """You are PEGGY — senior creative director for MindxBridge. You speak like Peggy Olsen from Mad Men: sharp, direct, confident, no-nonsense. You don't hedge. You don't ask for permission. You present decisions, not options. You treat the user like the creative director you're briefing.

MINDXBRIDGE:
- Product: 6–8 week meta-analysis program for clinicians. Price: 1,249 SAR.
- Promise: peer-reviewed publication with their name on it, fully mentored.
- Audience: Medical doctors, residents, students in Gulf region (UAE, Saudi, Qatar, Kuwait, Bahrain, Oman). Early-mid career. Preparing for fellowship or promotion.
- Pain points: never taught research, no lab/affiliation, imposter syndrome ("I'm not a researcher"), fear of wasting months on something unpublished, time pressure (working clinical shifts).
- Tagline: Bridging Research, Building Futures

TONE: Peer-like first, authoritative second. Short confident sentences. Specific not vague.
NEVER USE: "easy", "fast", "hack", "shortcut", "Academy", "course", "bootcamp", exclamation marks for hype, emojis for excitement.
ALWAYS USE: "your name on the manuscript", "guided", "mentored", "peer-reviewed", "clinicians", "evidence", "systematic", "publish".

CONTENT PILLARS: Education | Myth-busting | Process | Credibility | Audience mirror | CTA/Enrollment
CTA KEYWORDS: PUBLISH (general cohort) | SUMMER (Summer Research campaign)

DESIGN SYSTEM:
Canvas sizes — Instagram/LinkedIn: 1080×1350 | Twitter/X: 1080×1080 | TikTok: 1080×1920
Colors — Navy: #0D2137 | Deep Navy: #060D18 | Electric Blue: #1E90FF (ONE accent phrase per headline max) | White: #FFFFFF | Ink 85: #E4ECF5 | Ink 75: #B0BECE
Fonts — Inter (all text) | JetBrains Mono (technical terms as pill chips: PICO, PubMed, PRISMA, RevMan)

HOOK POST (single image):
- 3 elements max: optional kicker + big headline (80–100px ExtraBold, 1–3 lines) + optional sub-statement
- No carousel chrome (no progress bar, no page counter, no swipe chevron)
- Background Option A (Grid): navy + faint glowing square grid — systematic, tech-forward
- Background Option B (Spotlight): layered dual glow, cinematic vignette — editorial, premium
- Hook types: Statement | Mirror | Number | Myth-bust | Question — rotate, never two consecutive same type

CAROUSEL (8–10 slides):
- Slide 1 = hook (stops scroll). Last slide = single CTA only. One idea per slide.
- Block types: kicker | title | underline | body | bullets | steps | specs | card | button
- Every slide: white logo top-left, progress bar, page counter, mindxbridge.com footer

When given a brief, always deliver in this order:
1. Strategic angle (pillar, audience fear/desire targeted, hook type selected and why)
2. Full copy — headline, body, CTA
3. Design spec (background option, block-by-block Canva instructions)
4. Platform captions adapted for each relevant platform

State your creative choices as facts, not questions. Peggy doesn't say "what do you think?" She says "Here's what we're doing and why it works."
"""

STATUS_OPTS = ["BRIEF NEEDED", "IN PROGRESS", "AWAITING APPROVAL", "APPROVED", "DONE"]

# Session state
for key, val in {
    "hook_status": "BRIEF NEEDED",
    "carousel_status": "BRIEF NEEDED",
    "video_confirmed": False,
    "messages": [],
    "last_type": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

def status_icon(s):
    return {"DONE": "✅", "APPROVED": "✅", "AWAITING APPROVAL": "⏳", "IN PROGRESS": "🔵"}.get(s, "⬜")

def status_class(s):
    if s in ("DONE", "APPROVED"): return "status-done"
    if s == "AWAITING APPROVAL": return "status-wait"
    if s == "IN PROGRESS": return "status-active"
    return "status-idle"

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="top-line"></div>', unsafe_allow_html=True)
    st.markdown("### 🧠 MindxBridge")
    st.markdown('<span class="faint" style="font-size:0.8rem">mindxbridge.com</span>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown(f'<div class="sidebar-label">Week of {date.today().strftime("%d %b %Y")}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">This Week</div>', unsafe_allow_html=True)
    video_icon = "✅" if st.session_state.video_confirmed else "⬜"
    st.markdown(f"""
    <div class="card" style="margin-top:0.5rem">
      <div style="margin-bottom:0.5rem">
        {status_icon(st.session_state.hook_status)} <b>Hook Graphic</b><br>
        <span class="{status_class(st.session_state.hook_status)}">&nbsp;&nbsp;{st.session_state.hook_status}</span>
      </div>
      <div style="margin-bottom:0.5rem">
        {status_icon(st.session_state.carousel_status)} <b>Carousel</b><br>
        <span class="{status_class(st.session_state.carousel_status)}">&nbsp;&nbsp;{st.session_state.carousel_status}</span>
      </div>
      <div>
        {video_icon} <b>Video</b><br>
        <span class="status-idle">&nbsp;&nbsp;{"CONFIRMED" if st.session_state.video_confirmed else "EXTERNAL"}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<br><div class="sidebar-label">Update Status</div>', unsafe_allow_html=True)
    st.session_state.hook_status = st.selectbox("Hook", STATUS_OPTS, index=STATUS_OPTS.index(st.session_state.hook_status), key="hsel")
    st.session_state.carousel_status = st.selectbox("Carousel", STATUS_OPTS, index=STATUS_OPTS.index(st.session_state.carousel_status), key="csel")
    if st.button("✅ Video confirmed"):
        st.session_state.video_confirmed = True
        st.rerun()

    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Flags</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="flag">⚠ Logo: black backgrounds — need transparent PNGs</div>
    <div class="flag">⚠ Testimonials: zero captured</div>
    """, unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)
    if st.button("🔄 Reset week"):
        for k in ["hook_status", "carousel_status", "video_confirmed", "messages", "last_type"]:
            del st.session_state[k]
        st.rerun()

# ── MAIN ─────────────────────────────────────────────────────
st.markdown('<div class="top-line"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="peggy-header">
  <div class="peggy-title">PEG<span>GY</span></div>
  <div class="peggy-sub">MINDXBRIDGE CONTENT SYSTEM &nbsp;·&nbsp; SENIOR CREATIVE DIRECTOR</div>
</div>
""", unsafe_allow_html=True)

# API setup
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
except Exception:
    st.error("API key missing. Check `.streamlit/secrets.toml`.")
    st.stop()

# Brief input
st.markdown("#### Brief")
brief = st.text_area(
    "brief_input",
    placeholder='e.g. "Hook post — doctors don\'t need a lab — myth-busting" or "Carousel — what is PRISMA?" or "Campaign — enrollment opens Monday — 5 days"',
    height=90,
    label_visibility="collapsed"
)

post_type = st.radio(
    "Type",
    ["Hook Graphic", "Carousel", "Campaign", "Weekly Workflow"],
    horizontal=True
)

col1, col2 = st.columns([2, 5])
with col1:
    submit = st.button("→ Send to PEGGY", use_container_width=True)

st.markdown('<hr>', unsafe_allow_html=True)

# Generate
if submit and brief.strip():
    full_brief = f"[{post_type.upper()}] {brief.strip()}"
    st.session_state.last_type = post_type

    with st.spinner("PEGGY is working..."):
        try:
            resp = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2500,
                system=BRAND_SYSTEM,
                messages=[
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    {"role": "user", "content": full_brief}
                ]
            )
            answer = resp.content[0].text
            st.session_state.messages.append({"role": "user", "content": full_brief})
            st.session_state.messages.append({"role": "assistant", "content": answer})

            if post_type == "Hook Graphic":
                st.session_state.hook_status = "AWAITING APPROVAL"
            elif post_type == "Carousel":
                st.session_state.carousel_status = "AWAITING APPROVAL"

            st.rerun()
        except Exception as e:
            st.error(f"API error: {e}")

# Display output
if st.session_state.messages:
    latest_answer = st.session_state.messages[-1]["content"]
    latest_brief  = st.session_state.messages[-2]["content"]

    st.markdown(f'<div class="faint" style="font-size:0.8rem;margin-bottom:0.25rem">Brief: {latest_brief}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="response-box">{latest_answer}</div>', unsafe_allow_html=True)

    # Approval row
    st.markdown("**Your call:**")
    col_a, col_b, col_c = st.columns([1, 2, 2])
    with col_a:
        if st.button("✅ APPROVE"):
            t = st.session_state.last_type
            if t == "Hook Graphic":
                st.session_state.hook_status = "APPROVED"
            elif t == "Carousel":
                st.session_state.carousel_status = "APPROVED"
            st.success("Locked in.")
            st.rerun()
    with col_b:
        change_note = st.text_input("change_input", placeholder="What to change...", label_visibility="collapsed")
    with col_c:
        if st.button("✏ CHANGE"):
            if change_note.strip():
                with st.spinner("Revising..."):
                    try:
                        resp = client.messages.create(
                            model="claude-sonnet-4-6",
                            max_tokens=2500,
                            system=BRAND_SYSTEM,
                            messages=[
                                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                                {"role": "user", "content": f"Change: {change_note.strip()}"}
                            ]
                        )
                        revised = resp.content[0].text
                        st.session_state.messages.append({"role": "user", "content": f"Change: {change_note.strip()}"})
                        st.session_state.messages.append({"role": "assistant", "content": revised})
                        st.rerun()
                    except Exception as e:
                        st.error(f"API error: {e}")
            else:
                st.warning("Type what to change first.")

    # Session history
    if len(st.session_state.messages) > 2:
        with st.expander(f"Session history — {len(st.session_state.messages)//2} exchanges"):
            for i in range(0, len(st.session_state.messages)-2, 2):
                u = st.session_state.messages[i]["content"]
                a = st.session_state.messages[i+1]["content"]
                st.markdown(f"**You:** {u[:200]}{'...' if len(u)>200 else ''}")
                st.markdown(f"**PEGGY:** {a[:300]}{'...' if len(a)>300 else ''}")
                st.markdown("---")

else:
    st.markdown("""
    <div class="idle-quote">
      <div style="color:#E4ECF5;font-size:1.05rem;font-style:italic">"Two post slots open. The brief won't write itself."</div>
      <div class="faint" style="margin-top:0.5rem;font-size:0.82rem">— PEGGY</div>
    </div>
    """, unsafe_allow_html=True)
