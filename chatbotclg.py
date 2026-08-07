import streamlit as st
from google import genai

st.set_page_config(
    page_title="College Bot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# ---------- UI ----------
st.title("🎓 College Info Bot")
st.caption(
    "Ask me anything about colleges in Chennai — courses, admissions, and more."
)

# ---------- Show chat history ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- Chat input ----------
user_input = st.chat_input("Ask about a college...")

if user_input:

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare conversation history
    conversation = ""

    for msg in st.session_state.messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    # Get bot response
    with st.chat_message("assistant"):
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
    # ---------- Sidebar ----------
with st.sidebar:
    st.header("About")
    st.write(
        "This bot answers questions about colleges in Chennai "
        "using a fixed knowledge base."
    )

    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()
