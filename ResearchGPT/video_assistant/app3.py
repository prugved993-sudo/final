import gc
import os
import shutil
import tempfile

import streamlit as st

from .main import run_pipeline
from .core.rag_engine import ask_question


TEMP_DIR = "video_temp"


def clear_previous_data():
    """Clear previous session data and temporary files."""

    keys = [
        "video_result",
        "rag_chain",
        "video_source",
        "chat_history",
    ]

    for key in keys:
        if key in st.session_state:
            del st.session_state[key]

    gc.collect()

    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR, ignore_errors=True)

    os.makedirs(TEMP_DIR, exist_ok=True)


def run():

    st.title("🎥 AI Video Assistant")

    st.markdown(
        """
Analyze a **YouTube video** or a **local video** using AI.

Features:
- 🎙 Speech Transcription
- 📝 Summary
- ✅ Action Items
- 🔑 Key Decisions
- ❓ Open Questions
- 💬 Chat with Video (RAG)
"""
    )

    language = st.selectbox(
        "Select Language",
        ["english", "hinglish"],
    )

    tab1, tab2 = st.tabs(
        ["🔗 YouTube URL", "📁 Local Video"]
    )

    # -------------------------------------------------------
    # YouTube
    # -------------------------------------------------------

    with tab1:

        youtube_url = st.text_input(
            "Paste YouTube URL"
        )

        if st.button(
            "Analyze YouTube Video",
            key="youtube"
        ):

            if not youtube_url.strip():
                st.warning("Please enter a YouTube URL.")
                return

            clear_previous_data()

            with st.spinner("Processing video..."):

                result = run_pipeline(
                    youtube_url,
                    language,
                )

            st.session_state["video_result"] = result
            st.session_state["rag_chain"] = result["rag_chain"]

    # -------------------------------------------------------
    # Local Video
    # -------------------------------------------------------

    with tab2:

        uploaded_video = st.file_uploader(
            "Upload Video",
            type=["mp4", "mov", "avi", "mkv"],
        )

        if uploaded_video is not None:

            st.video(uploaded_video)

            if st.button(
                "Analyze Local Video",
                key="local"
            ):

                clear_previous_data()

                video_path = os.path.join(
                    TEMP_DIR,
                    uploaded_video.name,
                )

                with open(video_path, "wb") as f:
                    f.write(uploaded_video.getbuffer())

                with st.spinner("Processing video..."):

                    result = run_pipeline(
                        video_path,
                        language,
                    )

                st.session_state["video_result"] = result
                st.session_state["rag_chain"] = result["rag_chain"]

    # -------------------------------------------------------
    # Display Results
    # -------------------------------------------------------

    if "video_result" in st.session_state:

        result = st.session_state["video_result"]

        st.success("Analysis Completed!")

        tab_summary, tab_transcript, tab_chat = st.tabs(
            [
                "📋 Summary",
                "📄 Transcript",
                "💬 Chat",
            ]
        )

        with tab_summary:

            st.subheader("Summary")
            st.write(result["summary"])

            st.divider()

            st.subheader("Action Items")
            st.write(result["action_items"])

            st.divider()

            st.subheader("Key Decisions")
            st.write(result["key_decisions"])

            st.divider()

            st.subheader("Open Questions")
            st.write(result["open_questions"])

        with tab_transcript:

            st.subheader("Transcript")

            st.text_area(
                "",
                result["transcript"],
                height=450,
            )

        with tab_chat:

            question = st.chat_input(
                "Ask anything about the video..."
            )

            if question:

                with st.chat_message("user"):
                    st.write(question)

                answer = ask_question(
                    st.session_state["rag_chain"],
                    question,
                )

                with st.chat_message("assistant"):
                    st.write(answer)