import streamlit as st
from document_qa import app1
from deep_research import app2
from video_assistant import app3


st.set_page_config(
    page_title="ResearchGPT",
    page_icon="🧠",
    layout="wide"
)

# ---------- Session ----------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------- Sidebar ----------
with st.sidebar:
    st.title("🧠 ResearchGPT")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"

    if st.button("📄 Document QA", use_container_width=True):
        st.session_state.page = "Document QA"

    if st.button("🔍 Deep Research", use_container_width=True):
        st.session_state.page = "Deep Research"

    if st.button("🎥 Video Assistant", use_container_width=True):
        st.session_state.page = "Video Assistant"

# ---------- Home ----------
if st.session_state.page == "Home":

    st.title("🧠 ResearchGPT")
    st.subheader("One Platform for AI Research")

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("📄 Document QA")
        st.write("Ask questions from PDFs")
        if st.button("Explore Document QA"):
            st.session_state.page = "Document QA"
            st.rerun()

    with c2:
        st.info("🔍 Deep Research")
        st.write("Generate AI research reports")
        if st.button("Explore Deep Research"):
            st.session_state.page = "Deep Research"
            st.rerun()

    with c3:
        st.info("🎥 Video Assistant")
        st.write("Analyze YouTube videos")
        if st.button("Explore Video Assistant"):
            st.session_state.page = "Video Assistant"
            st.rerun()

    st.markdown("---")

    st.markdown("""
    ### Features

    - 📄 PDF Question Answering
    - 🔍 AI Research Agent
    - 🎥 Video Understanding
    - 🤖 OpenAI Powered
    - ⚡ Fast and Interactive
    """)

# ---------- Pages ----------
elif st.session_state.page == "Document QA":
    app1.run()

elif st.session_state.page == "Deep Research":
    app2.run()

elif st.session_state.page == "Video Assistant":
    app3.run()