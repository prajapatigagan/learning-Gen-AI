import os

import streamlit as st
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv(find_dotenv())

st.set_page_config(page_title="Movie Info Extractor", page_icon="🎬")
st.title("🎬 Movie Information Extractor")
st.caption("Movie ka paragraph paste karo, structured info mil jayegi.")

SYSTEM_PROMPT = """
You are a Professional Movie Information Extraction Assistant.
Your task:
Extract useful structured movie information from a movie paragraph and present it in a clear format.
Rules:
- Do NOT add explanations
- Do NOT add extra commentary
- Follow the exact format
- If information is missing -> write Null
- Keep summary short (2-3 lines max)
- Do NOT guess unknown facts

Output format:

Movie Title:
Release Year:
Genre:
Director:
Main Cast:
Setting/Location:
Plot:
Themes:
Ratings:
Notable Features:

Short Summary:
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "Extract information from this paragraph:\n{paragraph}"),
    ]
)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Settings")
    model_name = st.text_input("Model", "openrouter/free")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.1)
    st.caption("Extraction ke liye low temperature better hai.")


@st.cache_resource
def get_model(name: str, temp: float):
    return ChatOpenAI(
        model=name,
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=temp,
        max_completion_tokens=1000,
    )


chain = prompt | get_model(model_name, temperature)

# ---------- Input ----------
EXAMPLE = (
    "Inception is a 2010 sci-fi thriller directed by Christopher Nolan, "
    "starring Leonardo DiCaprio. A thief enters people's dreams to steal secrets."
)

if "paragraph" not in st.session_state:
    st.session_state.paragraph = ""

if st.button("Example paragraph daalo"):
    st.session_state.paragraph = EXAMPLE

para = st.text_area("Movie paragraph", key="paragraph", height=200)

if st.button("Extract", type="primary", use_container_width=True):
    if not para.strip():
        st.warning("Pehle paragraph likho.")
    else:
        with st.spinner("Extract ho raha hai..."):
            try:
                result = chain.invoke({"paragraph": para}).content
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

        st.subheader("Result")

        # key: value lines ko parse karke dikhao
        fields = {}
        for line in result.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                if key.strip():
                    fields[key.strip()] = value.strip()

        if fields:
            for key, value in fields.items():
                st.markdown(f"**{key}:** {value if value else 'Null'}")
        else:
            st.write(result)

        with st.expander("Raw output"):
            st.code(result)