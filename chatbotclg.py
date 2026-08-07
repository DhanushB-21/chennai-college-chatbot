import streamlit as st
from google import genai

st.set_page_config(
    page_title="College Bot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PREMIUM UI CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,0.13), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(168,85,247,0.10), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(59,130,246,0.08), transparent 35%),
        #080b14;
    color: #f8fafc;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 6rem !important;
    max-width: 1200px;
}


/* ---------- HIDE DEFAULT STREAMLIT UI ---------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* ---------- SIDEBAR ---------- */

with st.sidebar:
    st.markdown("## College Info AI")
    st.caption("Your intelligent guide to college information.")

    st.divider()

    st.markdown("### Explore")

    st.info("**Courses**\n\nExplore available programs and courses.")
    st.info("**Admissions**\n\nGet information about admission procedures.")
    st.info("**Campus**\n\nLearn about campus facilities and student life.")
    st.info("**Ask Anything**\n\nAsk questions about colleges in Chennai.")

    st.divider()

    st.markdown("### AI Online")
    st.caption("Ready to answer your questions.")

    st.divider()

    st.markdown("### About")
    st.caption(
        "This bot answers questions about colleges in Chennai "
        "using a fixed knowledge base."
    )

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

/* ---------- HERO ---------- */

st.markdown("""
<div class="hero">
    <div class="hero-content">
        <div class="status">
            <span class="status-dot"></span>
            AI ASSISTANT • ONLINE
        </div>

        <h1 class="hero-title">
            Find the right college.<br>
            Ask anything.
        </h1>

        <div class="hero-description">
            Your intelligent guide to colleges in Chennai —
            explore courses, admissions, facilities and more.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
/* ---------- QUICK QUESTIONS ---------- */

.quick-title {
    color: #64748b;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;

    margin: 20px 0 10px 3px;
}

.quick-card {
    padding: 14px;

    min-height: 90px;

    border-radius: 16px;

    background: rgba(255,255,255,0.035);

    border: 1px solid rgba(255,255,255,0.06);

    transition: all 0.25s ease;
}

.quick-card:hover {
    transform: translateY(-2px);

    border-color: rgba(129,140,248,0.35);

    background: rgba(99,102,241,0.08);

    box-shadow:
        0 10px 30px rgba(0,0,0,0.18);
}

.quick-icon {
    font-size: 20px;
    margin-bottom: 7px;
}

.quick-card-title {
    font-size: 12px;
    font-weight: 600;
    color: #e2e8f0;
}

.quick-card-text {
    font-size: 10px;
    color: #64748b;
    margin-top: 3px;
}


/* ---------- CHAT ---------- */

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;

    padding-top: 8px !important;
    padding-bottom: 8px !important;
}

[data-testid="stChatMessageContent"] {
    border-radius: 18px !important;

    padding: 15px 18px !important;

    font-size: 14px !important;
    line-height: 1.65 !important;
}


/* Assistant message */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
)
[data-testid="stChatMessageContent"] {

    background:
        linear-gradient(
            135deg,
            rgba(30,41,59,0.75),
            rgba(15,23,42,0.75)
        ) !important;

    border:
        1px solid rgba(255,255,255,0.07) !important;

    box-shadow:
        0 10px 35px rgba(0,0,0,0.12);
}


/* User message */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
)
[data-testid="stChatMessageContent"] {

    background:
        linear-gradient(
            135deg,
            rgba(79,70,229,0.9),
            rgba(124,58,237,0.88)
        ) !important;

    border:
        1px solid rgba(167,139,250,0.25) !important;

    box-shadow:
        0 10px 35px rgba(79,70,229,0.15);
}


/* ---------- CHAT INPUT ---------- */

[data-testid="stChatInput"] {
    position: fixed;

    bottom: 20px;

    left: 50%;

    transform: translateX(-50%);

    width: min(850px, 90vw);

    z-index: 999;
}

[data-testid="stChatInput"] > div {
    background: rgba(15,23,42,0.92) !important;

    border:
        1px solid rgba(255,255,255,0.12) !important;

    border-radius: 20px !important;

    box-shadow:
        0 15px 50px rgba(0,0,0,0.45),
        0 0 0 1px rgba(99,102,241,0.05);

    backdrop-filter: blur(20px);
}

[data-testid="stChatInput"] textarea {
    color: #f8fafc !important;

    font-size: 14px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
}


/* ---------- BUTTONS ---------- */

.stButton > button {
    border-radius: 12px;

    border: 1px solid rgba(255,255,255,0.08);

    background: rgba(255,255,255,0.04);

    color: #cbd5e1;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: rgba(129,140,248,0.4);

    background: rgba(99,102,241,0.12);

    color: #ffffff;
}


/* ---------- MOBILE ---------- */

@media (max-width: 768px) {

    .block-container {
        padding: 1rem 0.8rem 6rem !important;
    }

    [data-testid="stSidebar"] {
        min-width: 260px;
    }

    .hero {
        padding: 22px 20px;

        border-radius: 20px;

        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 28px;
    }

    .hero-description {
        font-size: 13px;
    }

    .quick-card {
        min-height: 75px;
        padding: 11px;
    }

    .quick-icon {
        font-size: 17px;
    }

    .quick-card-title {
        font-size: 11px;
    }

    .quick-card-text {
        display: none;
    }

    [data-testid="stChatMessageContent"] {
        font-size: 13px !important;

        padding: 12px 14px !important;
    }

    [data-testid="stChatInput"] {
        width: 94vw;

        bottom: 10px;
    }
}


/* ---------- SMALL PHONES ---------- */

@media (max-width: 420px) {

    .hero {
        padding: 18px;
    }

    .hero-title {
        font-size: 24px;
    }

    .status {
        font-size: 10px;
    }

    [data-testid="stChatInput"] {
        width: 96vw;
    }
}

</style>
""", unsafe_allow_html=True)


# ---------- Load knowledge base ----------
with open("college_details.txt", "r", encoding="utf-8") as f:
    kb = f.read()

# ---------- Build system prompt ----------
prompt = f"""
You are the Chennai College Info Bot for students who have completed 12th grade.

Your job is to provide information about colleges in Chennai.

Rules:
1. Answer politely and clearly.
2. Only use the information provided in the knowledge base below.
3. If the answer is not available in the knowledge base, say:
   "Sorry, I don't have that information in my college database."
4. Do not make up or guess information.

KNOWLEDGE BASE:
{kb}
"""

# ---------- Gemini client ----------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

model = "gemini-flash-latest"

# ---------- Initialize messages ----------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# PREMIUM UI
# ============================================================

# ---------- Hero Header ----------

st.markdown("""
<div class="hero">

    <div class="hero-content">

        <div class="status">
            <span class="status-dot"></span>
            AI ASSISTANT • ONLINE
        </div>

        <h1 class="hero-title">
            Find the right college.<br>
            Ask anything.
        </h1>

        <div class="hero-description">
            Your intelligent guide to colleges in Chennai —
            explore courses, admissions, facilities and more.
        </div>

    </div>

</div>
""", unsafe_allow_html=True)


# ---------- Quick Questions ----------

if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="quick-title">Popular questions</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="quick-card">
            <div class="quick-icon">🎓</div>
            <div class="quick-card-title">
                What courses are available?
            </div>
            <div class="quick-card-text">
                Explore programs and courses.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="quick-card">
            <div class="quick-icon">📝</div>
            <div class="quick-card-title">
                How does admission work?
            </div>
            <div class="quick-card-text">
                Learn about admission procedures.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="quick-card">
            <div class="quick-icon">🏫</div>
            <div class="quick-card-title">
                Tell me about the campus
            </div>
            <div class="quick-card-text">
                Discover campus facilities.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ---------- Show chat history ----------
for msg in st.session_state.messages:

    avatar = "🤖" if msg["role"] == "assistant" else "👤"

    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# ---------- Chat input ----------
user_input = st.chat_input("Ask about a college, course, admission...")


if user_input:

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Prepare conversation history
    conversation = ""

    for msg in st.session_state.messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    # Get bot response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):

            response = client.models.generate_content(
                model=model,
                contents=f"""
{prompt}

Conversation:
{conversation}

Answer the user's latest question using ONLY the knowledge base.
"""
            )

            answer = response.text
            st.markdown(answer)

    # Save bot response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">

        <div class="sidebar-logo">
            🎓
        </div>

        <div class="sidebar-title">
            College Info AI
        </div>

        <div class="sidebar-subtitle">
            Your intelligent guide to college information.
        </div>

    </div>
    """, unsafe_allow_html=True)


    st.markdown(
        '<div class="sidebar-section">Explore</div>',
        unsafe_allow_html=True
    )


    st.markdown("""
    <div class="sidebar-card">

        <div class="sidebar-card-title">
            📚 Courses
        </div>

        <div class="sidebar-card-text">
            Explore available programs and courses.
        </div>

    </div>


    <div class="sidebar-card">

        <div class="sidebar-card-title">
            🎯 Admissions
        </div>

        <div class="sidebar-card-text">
            Get information about admission procedures.
        </div>

    </div>


    <div class="sidebar-card">

        <div class="sidebar-card-title">
            🏫 Campus
        </div>

        <div class="sidebar-card-text">
            Learn about campus facilities and student life.
        </div>

    </div>


    <div class="sidebar-card">

        <div class="sidebar-card-title">
            💡 Ask Anything
        </div>

        <div class="sidebar-card-text">
            Ask questions about colleges in Chennai.
        </div>

    </div>
    """, unsafe_allow_html=True)


    st.markdown(
        '<div class="sidebar-section">AI Status</div>',
        unsafe_allow_html=True
    )


    st.markdown("""
    <div class="sidebar-card">

        <div style="
            display:flex;
            align-items:center;
            gap:8px;
            color:#86efac;
            font-size:12px;
            font-weight:600;
        ">

            <span style="
                width:7px;
                height:7px;
                border-radius:50%;
                background:#22c55e;
                box-shadow:0 0 10px #22c55e;
            "></span>

            AI Online

        </div>

        <div class="sidebar-card-text">
            Ready to answer your questions.
        </div>

    </div>
    """, unsafe_allow_html=True)


    # ---------- Your original About section ----------
    st.markdown(
        '<div class="sidebar-section">About</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="sidebar-card">

        <div class="sidebar-card-text">
            This bot answers questions about colleges in Chennai
            using a fixed knowledge base.
        </div>

    </div>
    """, unsafe_allow_html=True)


    # ---------- Your original Clear Chat button ----------
    if st.button("🗑️ Clear chat"):

        st.session_state.messages = []

        st.rerun()
