import streamlit as st
from google import genai

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="College Bot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

try:
    with open("college_details.txt", "r", encoding="utf-8") as f:
        kb = f.read()
except FileNotFoundError:
    st.error("college_details.txt was not found.")
    st.stop()

# ============================================================
# SYSTEM PROMPT
# ============================================================

system_prompt = f"""
You are the Chennai College Info Bot for students who have
completed 12th grade.

Your job is to provide information about colleges in Chennai.

RULES:

1. Answer politely and clearly.
2. ONLY use information provided in the knowledge base below.
3. If the answer is not available in the knowledge base, say:
   "Sorry, I don't have that information in my college database."
4. Never make up, guess, or assume information.
5. Keep answers relevant to the user's question.

KNOWLEDGE BASE:
{kb}
"""

# ============================================================
# GEMINI CLIENT
# ============================================================

try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"],
        http_options={"api_version": "v1"}
    )
except Exception:
    st.error("Unable to initialize Gemini. Please check your API key.")
    st.stop()

# Use a stable model instead of the moving "latest" alias.
model = "gemini-3.6-flash"

# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# UI
# ============================================================

st.title("🎓 College Info Bot")

st.caption(
    "Ask me anything about colleges in Chennai — "
    "courses, admissions, eligibility, and more."
)

# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input("Ask about a college...")

if user_input:

    # --------------------------------------------------------
    # Save and display user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # --------------------------------------------------------
    # Build conversation
    # --------------------------------------------------------

    conversation = ""

    for msg in st.session_state.messages:
        conversation += (
            f"{msg['role'].upper()}: {msg['content']}\n"
        )

    # --------------------------------------------------------
    # Generate response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=f"""
{system_prompt}

CONVERSATION:
{conversation}

IMPORTANT:
Answer ONLY the latest user question.
Use ONLY the knowledge base.
If the information is not present in the knowledge base, reply:

"Sorry, I don't have that information in my college database."
"""
                )

                answer = response.text

                if not answer:
                    answer = (
                        "Sorry, I couldn't generate a response right now."
                    )

                st.markdown(answer)

            except Exception as e:

                answer = (
                    "⚠️ Gemini is temporarily unavailable. "
                    "Please try again in a moment."
                )

                st.markdown(answer)

                # Show technical error only in the app logs
                print("Gemini API Error:", repr(e))

    # --------------------------------------------------------
    # Save assistant response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🎓 About")

    st.write(
        "This bot answers questions about colleges in Chennai "
        "using a fixed college knowledge base."
    )

    st.divider()

    st.subheader("💬 What can I ask?")

    st.write(
        """
        • Colleges  
        • Courses  
        • Admissions  
        • Eligibility  
        • Fees  
        • Departments  
        • Contact information
        """
    )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()
```
