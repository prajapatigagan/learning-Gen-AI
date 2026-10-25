import os
import streamlit as st

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


# =====================================================
# 1. CONFIGURATION
# =====================================================

load_dotenv()

st.set_page_config(
    page_title="MoodAI Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0b1020 0%,
        #111827 55%,
        #211449 100%
    );
    color: #f8fafc;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #293449;
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 850;
    text-align: center;
    background: linear-gradient(
        90deg,
        #a78bfa,
        #38bdf8,
        #f0abfc
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

.hero-subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 2rem;
}

.mode-card {
    min-height: 185px;
    padding: 22px 12px;
    border-radius: 18px;
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.12);
    text-align: center;
    margin-bottom: 10px;
    transition: 0.2s ease;
}

.mode-emoji {
    font-size: 2.7rem;
}

.mode-name {
    font-size: 1.2rem;
    font-weight: 750;
    color: #f8fafc;
    margin-top: 8px;
}

.mode-description {
    color: #cbd5e1;
    font-size: 0.85rem;
    margin-top: 8px;
}

.stButton > button {
    width: 100%;
    min-height: 43px;
    border-radius: 12px;
    background: linear-gradient(90deg, #7c3aed, #4f46e5);
    color: white;
    border: 1px solid rgba(255,255,255,0.15);
    font-weight: 650;
    transition: 0.2s ease;
}

.stButton > button:hover {
    border-color: #c4b5fd;
    color: white;
    transform: translateY(-2px);
}

div[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 12px;
}

.info-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    padding: 16px;
    margin: 10px 0;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.85rem;
    margin-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. AI MODES
# =====================================================

MODES = {
    "Angry Mode": {
        "emoji": "😡",
        "description": "Attitude, sarcasm and spicy replies",
        "button": "😡 Choose Angry",
        "prompt": """
You are MoodAI King in Angry Mode.

Your personality:
- Be dramatic, sarcastic, impatient and fiery.
- Use playful attitude and witty comebacks.
- Keep the conversation entertaining.
- Do not use genuinely abusive or threatening language.
- Give accurate and useful answers to serious questions.
- Reply in the language used by the user.
- If the user speaks Hindi or Hinglish, respond in Hindi or Hinglish.
- Your name is King.
"""
    },

    "Funny Mode": {
        "emoji": "😂",
        "description": "Jokes, comedy and unlimited fun",
        "button": "😂 Choose Funny",
        "prompt": """
You are MoodAI King in Funny Mode.

Your personality:
- Be funny, witty, friendly and entertaining.
- Use jokes, clever observations and playful humor.
- Use emojis naturally.
- Avoid offensive or harmful jokes.
- Give accurate and helpful answers.
- Reply in the language used by the user.
- If the user speaks Hindi or Hinglish, respond in Hindi or Hinglish.
- Your name is King.
"""
    },

    "Sad Mode": {
        "emoji": "😢",
        "description": "Emotional, calm and thoughtful replies",
        "button": "😢 Choose Sad",
        "prompt": """
You are MoodAI King in Sad Mode.

Your personality:
- Speak in a calm, emotional and thoughtful tone.
- Use gentle language and reflective expressions.
- Be empathetic when the user shares a problem.
- Do not encourage hopelessness or self-harm.
- Continue to give practical and helpful advice.
- Reply in the language used by the user.
- If the user speaks Hindi or Hinglish, respond in Hindi or Hinglish.
- Your name is King.
"""
    }
}


# =====================================================
# 4. SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_mode" not in st.session_state:
    st.session_state.current_mode = "Funny Mode"


# =====================================================
# 5. MOOD SWITCH FUNCTION
# =====================================================

def change_mode(mode):
    if mode != st.session_state.current_mode:
        st.session_state.current_mode = mode
        st.session_state.messages = []


# =====================================================
# 6. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("# 🤖 MoodAI")
    st.caption("Your mood. Your AI. Your rules.")

    st.divider()

    current_mode = st.session_state.current_mode
    current_info = MODES[current_mode]

    st.markdown("### 🎭 Current Mood")

    st.markdown(
        f"""
        <div class="info-card">
            <div style="font-size:2.5rem;">
                {current_info['emoji']}
            </div>
            <h3>{current_mode}</h3>
            <p style="color:#cbd5e1;">
                {current_info['description']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ⚙️ Settings")

    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.markdown("### 📊 Chat Statistics")
    st.metric("Total Messages", len(st.session_state.messages))

    st.markdown("---")
    st.caption("Powered by Python, Streamlit & LangChain")


# =====================================================
# 7. HEADER
# =====================================================

st.markdown(
    '<div class="hero-title">MoodAI Studio ✨</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Choose your AI personality and start a conversation.'
    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# 8. MOOD SELECTION ON MAIN SCREEN
# =====================================================

st.markdown("## 🎭 Choose Your AI Mood")

st.caption("Select a personality below. You can change it anytime.")

col1, col2, col3 = st.columns(3)

mode_columns = [col1, col2, col3]
mode_names = ["Angry Mode", "Funny Mode", "Sad Mode"]

for column, mode_name in zip(mode_columns, mode_names):

    info = MODES[mode_name]

    with column:

        st.markdown(
            f"""
            <div class="mode-card">
                <div class="mode-emoji">{info['emoji']}</div>
                <div class="mode-name">{mode_name}</div>
                <div class="mode-description">
                    {info['description']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if mode_name == st.session_state.current_mode:
            button_label = f"✅ Selected: {mode_name}"
        else:
            button_label = info["button"]

        if st.button(
            button_label,
            key=f"select_{mode_name}",
            use_container_width=True
        ):
            if mode_name != st.session_state.current_mode:
                change_mode(mode_name)
                st.rerun()


# =====================================================
# 9. ACTIVE MODE STATUS
# =====================================================

selected_mode = st.session_state.current_mode
mode_info = MODES[selected_mode]

st.markdown(
    f"""
    <div class="info-card">
        <b>{mode_info['emoji']} Active Mode: {selected_mode}</b>
        <br>
        <span style="color:#cbd5e1;">
            {mode_info['description']}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =====================================================
# 10. API CONFIGURATION
# =====================================================

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error(
        "OPENROUTER_API_KEY nahi mili. "
        "Project ki .env file check karo."
    )
    st.stop()


# =====================================================
# 11. MODEL CONFIGURATION
# =====================================================

@st.cache_resource
def get_model():
    return ChatOpenAI(
        model="openrouter/free",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0.7,
        max_tokens=500
    )


model = get_model()


# =====================================================
# 12. WELCOME MESSAGE
# =====================================================

if not st.session_state.messages:

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:28px 15px;
            background:rgba(255,255,255,0.035);
            border-radius:20px;
            border:1px solid rgba(255,255,255,0.08);
        ">
            <div style="font-size:3rem;">
                {mode_info['emoji']}
            </div>
            <h2>Hey there! 👋</h2>
            <p style="color:#cbd5e1;">
                Welcome to <b>{selected_mode}</b>.
            </p>
            <p style="color:#94a3b8;">
                Type a message below to start chatting with King.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 13. DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    if message["role"] == "user":
        avatar = "🧑‍💻"
    else:
        avatar = mode_info["emoji"]

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# =====================================================
# 14. CHAT INPUT AND AI RESPONSE
# =====================================================

prompt = st.chat_input("💬 Type your message here...")


if prompt:

    # Add the user's message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Prepare conversation history
    langchain_messages = [
        SystemMessage(content=mode_info["prompt"])
    ]

    for message in st.session_state.messages:

        if message["role"] == "user":
            langchain_messages.append(
                HumanMessage(content=message["content"])
            )

        else:
            langchain_messages.append(
                AIMessage(content=message["content"])
            )

    # Generate response
    with st.chat_message("assistant", avatar=mode_info["emoji"]):

        with st.spinner(f"{selected_mode} is thinking..."):

            try:
                response = model.invoke(langchain_messages)

                answer = response.content

                if not isinstance(answer, str):
                    answer = str(answer)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:

                # Remove the unanswered user message
                if (
                    st.session_state.messages
                    and st.session_state.messages[-1]["role"] == "user"
                ):
                    st.session_state.messages.pop()

                st.error("AI response generate nahi ho paya.")
                st.caption(f"Error details: {error}")


# =====================================================
# 15. FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer">
        Made with ❤️ | MoodAI Studio | Python + Streamlit + LangChain
    </div>
    """,
    unsafe_allow_html=True
)

