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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
    box-sizing: border-box;
}

.stApp {
    background: #060D18;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(22,78,134,0.35) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(30,144,255,0.08) 0%, transparent 50%);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: rgba(4, 9, 18, 0.97) !important;
    border-right: 1px solid rgba(30,144,255,0.12) !important;
}
section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

/* ── MAIN CONTAINER ── */
.main .block-container {
    padding: 2.5rem 3rem 3rem 3rem;
    max-width: 860px;
}

/* ── TYPOGRAPHY ── */
h1, h2, h3, h4 { color: #FFFFFF !important; font-family: 'Inter', sans-serif !important; }
p, li, div { color: #E4ECF5; }

/* ── HEADER ── */
.peggy-wrap {
    padding-bottom: 2rem;
    border-bottom: 1px solid rgba(30,144,255,0.1);
    margin-bottom: 2rem;
}
.top-accent {
    width: 48px; height: 3px;
    background: #1E90FF;
    border-radius: 2px;
    margin-bottom: 1.2rem;
}
.peggy-title {
    font-size: 3.2rem;
    font-weight: 900;
    color: #FFFFFF;
    letter-spacing: -2px;
    line-height: 1;
    margin: 0 0 0.4rem 0;
}
.peggy-title em { color: #1E90FF; font-style: normal; }
.peggy-sub {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem;
    color: #687C94;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── SIDEBAR ELEMENTS ── */
.sb-brand { margin-bottom: 1.5rem; }
.sb-brand-name {
    font-size: 1rem; font-weight: 700; color: #FFFFFF;
}
.sb-brand-url {
    font-size: 0.75rem; color: #687C94;
    font-family: 'JetBrains Mono', monospace !important;
}
.sb-section-label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem; color: #687C94;
    letter-spacing: 2px; text-transform: uppercase;
    margin: 1.25rem 0 0.6rem 0;
}
.sb-divider {
    height: 1px;
    background: rgba(30,144,255,0.1);
    margin: 1rem 0;
}

/* ── CHECKLIST CARD ── */
.checklist-card {
    background: rgba(30,144,255,0.04);
    border: 1px solid rgba(30,144,255,0.12);
    border-radius: 12px;
    padding: 1rem 1.1rem;
}
.checklist-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.checklist-row:last-child { border-bottom: none; }
.checklist-label { font-size: 0.88rem; font-weight: 600; color: #E4ECF5; }
.status-pill {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.62rem; font-weight: 700;
    border-radius: 4px; padding: 2px 7px;
    letter-spacing: 0.5px;
}
.pill-idle    { background: rgba(104,124,148,0.15); color: #687C94; }
.pill-active  { background: rgba(30,144,255,0.15);  color: #1E90FF; }
.pill-wait    { background: rgba(255,179,71,0.15);  color: #FFB347; }
.pill-done    { background: rgba(76,175,80,0.15);   color: #4CAF50; }

/* ── FLAG ITEMS ── */
.flag-row {
    display: flex; gap: 0.5rem; align-items: flex-start;
    padding: 0.3rem 0;
    font-size: 0.8rem; color: #B0BECE;
}
.flag-dot { color: #FFB347; flex-shrink: 0; margin-top: 1px; }

/* ── INPUTS ── */
.stTextArea > div > textarea {
    background: rgba(6,13,24,0.8) !important;
    color: #E4ECF5 !important;
    border: 1px solid rgba(30,144,255,0.2) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    line-height: 1.6 !important;
    padding: 0.85rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextArea > div > textarea:focus {
    border-color: #1E90FF !important;
    box-shadow: 0 0 0 3px rgba(30,144,255,0.12) !important;
}
.stTextInput > div > input {
    background: rgba(6,13,24,0.8) !important;
    color: #E4ECF5 !important;
    border: 1px solid rgba(30,144,255,0.2) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.6rem 0.9rem !important;
}
.stTextInput > div > input::placeholder { color: #687C94 !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: #1E90FF !important;
    color: #060D18 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.4rem !important;
    letter-spacing: 0.2px !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 2px 12px rgba(30,144,255,0.25) !important;
}
.stButton > button:hover {
    background: #3da0ff !important;
    box-shadow: 0 4px 20px rgba(30,144,255,0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── RADIO ── */
.stRadio > div {
    background: rgba(6,13,24,0.6);
    border: 1px solid rgba(30,144,255,0.12);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    gap: 0.5rem;
}
.stRadio label { color: #B0BECE !important; font-size: 0.88rem !important; }

/* ── SELECT BOX ── */
.stSelectbox > div > div {
    background: rgba(6,13,24,0.8) !important;
    border: 1px solid rgba(30,144,255,0.2) !important;
    border-radius: 8px !important;
    color: #E4ECF5 !important;
}

/* ── RESPONSE BOX ── */
.response-box {
    background: rgba(6,13,24,0.6);
    border: 1px solid rgba(30,144,255,0.15);
    border-left: 3px solid #1E90FF;
    border-radius: 0 12px 12px 0;
    padding: 1.75rem 2rem;
    margin: 1.25rem 0;
    color: #E4ECF5;
    line-height: 1.8;
    font-size: 0.93rem;
    white-space: pre-wrap;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}

/* ── BRIEF LABEL ── */
.brief-label {
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace !important;
    color: #687C94;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
    padding: 0.3rem 0.6rem;
    background: rgba(30,144,255,0.06);
    border-radius: 4px;
    display: inline-block;
}

/* ── APPROVAL ROW ── */
.approval-label {
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace !important;
    color: #687C94;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── IDLE STATE ── */
.idle-box {
    background: rgba(6,13,24,0.5);
    border: 1px solid rgba(30,144,255,0.08);
    border-radius: 14px;
    padding: 3rem 2rem;
    text-align: center;
    margin-top: 1rem;
}
.idle-quote {
    font-size: 1.15rem;
    font-style: italic;
    color: #B0BECE;
    line-height: 1.6;
}
.idle-attr {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem;
    color: #687C94;
    margin-top: 0.75rem;
    letter-spacing: 1px;
}

hr { border: none; border-top: 1px solid rgba(30,144,255,0.1); margin: 1rem 0; }


/* ── SECTION TITLE ── */
.section-title {
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace !important;
    color: #687C94;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
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

def pill_class(s):
    return {"DONE": "pill-done", "APPROVED": "pill-done",
            "AWAITING APPROVAL": "pill-wait", "IN PROGRESS": "pill-active"}.get(s, "pill-idle")

def status_icon(s):
    return {"DONE": "✅", "APPROVED": "✅", "AWAITING APPROVAL": "⏳", "IN PROGRESS": "🔵"}.get(s, "⬜")

for key, val in {
    "hook_status": "BRIEF NEEDED", "carousel_status": "BRIEF NEEDED",
    "video_confirmed": False, "messages": [], "last_type": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="sb-brand">
        <div style="font-size:1.5rem;margin-bottom:0.4rem">🧠</div>
        <div class="sb-brand-name">MindxBridge</div>
        <div class="sb-brand-url">mindxbridge.com</div>
    </div>
    <div class="sb-divider"></div>
    <div class="sb-section-label">Week of {date.today().strftime("%d %b %Y")}</div>
    <div class="checklist-card">
        <div class="checklist-row">
            <span class="checklist-label">{status_icon(st.session_state.hook_status)} Hook Graphic</span>
            <span class="status-pill {pill_class(st.session_state.hook_status)}">{st.session_state.hook_status}</span>
        </div>
        <div class="checklist-row">
            <span class="checklist-label">{status_icon(st.session_state.carousel_status)} Carousel</span>
            <span class="status-pill {pill_class(st.session_state.carousel_status)}">{st.session_state.carousel_status}</span>
        </div>
        <div class="checklist-row">
            <span class="checklist-label">{"✅" if st.session_state.video_confirmed else "⬜"} Video</span>
            <span class="status-pill pill-idle">{"CONFIRMED" if st.session_state.video_confirmed else "EXTERNAL"}</span>
        </div>
    </div>
    <div class="sb-section-label">Update Status</div>
    """, unsafe_allow_html=True)

    st.session_state.hook_status = st.selectbox("Hook", STATUS_OPTS, index=STATUS_OPTS.index(st.session_state.hook_status), key="hsel", label_visibility="collapsed")
    st.session_state.carousel_status = st.selectbox("Carousel", STATUS_OPTS, index=STATUS_OPTS.index(st.session_state.carousel_status), key="csel", label_visibility="collapsed")

    if st.button("✅ Video confirmed", use_container_width=True):
        st.session_state.video_confirmed = True
        st.rerun()

    st.markdown("""
    <div class="sb-divider"></div>
    <div class="sb-section-label">Flags</div>
    <div class="flag-row"><span class="flag-dot">▲</span><span>Logo files have black backgrounds — need transparent PNGs</span></div>
    <div class="flag-row"><span class="flag-dot">▲</span><span>Testimonials: none captured yet</span></div>
    <div class="sb-divider"></div>
    """, unsafe_allow_html=True)

    if st.button("↺ Reset week", use_container_width=True):
        for k in ["hook_status", "carousel_status", "video_confirmed", "messages", "last_type"]:
            del st.session_state[k]
        st.rerun()

# ── MAIN ─────────────────────────────────────────────────────
st.markdown("""
<div class="peggy-wrap">
    <div class="top-accent"></div>
    <div class="peggy-title">PEG<em>GY</em></div>
    <div class="peggy-sub">MindxBridge Content System &nbsp;·&nbsp; Senior Creative Director</div>
</div>
""", unsafe_allow_html=True)

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
except Exception:
    st.error("API key missing. Check `.streamlit/secrets.toml`.")
    st.stop()

st.markdown('<div class="section-title">Brief</div>', unsafe_allow_html=True)
brief = st.text_area(
    "brief_input",
    placeholder='e.g. "Hook post — doctors don\'t need a lab — myth-busting" or "Carousel — what is PRISMA?" or "Campaign — enrollment opens Monday — 5 days"',
    height=95,
    label_visibility="collapsed"
)

post_type = st.radio("Type", ["Hook Graphic", "Carousel", "Campaign", "Weekly Workflow"], horizontal=True)

col1, col2 = st.columns([1, 4])
with col1:
    submit = st.button("→ Send to PEGGY", use_container_width=True)

st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)

if submit and brief.strip():
    full_brief = f"[{post_type.upper()}] {brief.strip()}"
    st.session_state.last_type = post_type

    with st.spinner(""):
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
            st.error(f"Error: {e}")

if st.session_state.messages:
    latest_brief  = st.session_state.messages[-2]["content"]
    latest_answer = st.session_state.messages[-1]["content"]

    st.markdown(f'<div class="brief-label">{latest_brief}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="response-box">{latest_answer}</div>', unsafe_allow_html=True)

    st.markdown('<div class="approval-label">Your call</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_a:
        if st.button("✅  APPROVE", use_container_width=True):
            t = st.session_state.last_type
            if t == "Hook Graphic": st.session_state.hook_status = "APPROVED"
            elif t == "Carousel":   st.session_state.carousel_status = "APPROVED"
            st.success("Locked in.")
            st.rerun()
    with col_b:
        change_note = st.text_input("change", placeholder="What to change...", label_visibility="collapsed")
    with col_c:
        if st.button("✏  CHANGE", use_container_width=True):
            if change_note.strip():
                with st.spinner(""):
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
                        st.error(f"Error: {e}")

    if len(st.session_state.messages) > 2:
        with st.expander(f"History — {len(st.session_state.messages)//2} exchanges"):
            for i in range(0, len(st.session_state.messages)-2, 2):
                u = st.session_state.messages[i]["content"]
                a = st.session_state.messages[i+1]["content"]
                st.markdown(f"**You:** {u[:200]}{'...' if len(u)>200 else ''}")
                st.markdown(f"**PEGGY:** {a[:300]}{'...' if len(a)>300 else ''}")
                st.markdown("---")
else:
    st.markdown("""
    <div class="idle-box">
        <div class="idle-quote">"Two post slots open.<br>The brief won't write itself."</div>
        <div class="idle-attr">— PEGGY</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
.sprite-wrap {
    position: fixed;
    bottom: 36px;
    right: 60px;
    z-index: 99999;
    animation: sbounce 0.45s ease-in-out infinite alternate,
               sdrift  10s  ease-in-out infinite alternate;
    filter: drop-shadow(0 0 7px rgba(30,144,255,0.7));
    pointer-events: none;
}
@keyframes sbounce {
    0%   { transform: translateY(0)    scaleY(1);    }
    100% { transform: translateY(-16px) scaleY(0.92); }
}
@keyframes sdrift {
    0%   { right: 60px;  }
    25%  { right: 200px; }
    50%  { right: 100px; }
    75%  { right: 280px; }
    100% { right: 60px;  }
}
</style>
<div class="sprite-wrap">
<svg width="36" height="60" viewBox="0 0 6 10" xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges">
  <rect x="1" y="0" width="4" height="1" fill="#1E90FF"/>
  <rect x="0" y="1" width="6" height="1" fill="#1E90FF"/>
  <rect x="0" y="2" width="1" height="1" fill="#1E90FF"/>
  <rect x="1" y="2" width="1" height="1" fill="#060D18"/>
  <rect x="4" y="2" width="1" height="1" fill="#060D18"/>
  <rect x="5" y="2" width="1" height="1" fill="#1E90FF"/>
  <rect x="2" y="2" width="2" height="1" fill="#1E90FF"/>
  <rect x="0" y="3" width="6" height="1" fill="#1E90FF"/>
  <rect x="2" y="4" width="2" height="1" fill="#1E90FF"/>
  <rect x="0" y="5" width="6" height="1" fill="#1E90FF"/>
  <rect x="0" y="6" width="1" height="1" fill="#1E90FF"/>
  <rect x="5" y="6" width="1" height="1" fill="#1E90FF"/>
  <rect x="0" y="7" width="1" height="1" fill="#1E90FF"/>
  <rect x="5" y="7" width="1" height="1" fill="#1E90FF"/>
</svg>
</div>
""", unsafe_allow_html=True)
