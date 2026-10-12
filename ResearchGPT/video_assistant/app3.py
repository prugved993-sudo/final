
import gc
import os
import shutil

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
Analyze a **local video file** using AI.

### Features
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

    st.markdown("---")
    st.subheader("📁 Upload Local Video")

    uploaded_video = st.file_uploader(
        "Choose a video file",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="local_video_uploader",
    )

    if uploaded_video is not None:

        st.video(uploaded_video)

        if st.button(
            "🎬 Analyze Local Video",
            key="local",
            use_container_width=True,
        ):

            clear_previous_data()

            os.makedirs(TEMP_DIR, exist_ok=True)

            # Save uploaded video using a temporary file path
            video_path = os.path.join(
                TEMP_DIR,
                os.path.basename(uploaded_video.name),
            )

            with open(video_path, "wb") as f:
                f.write(uploaded_video.getbuffer())

            try:
                with st.spinner(
                    "Processing local video... Please wait."
                ):
                    result = run_pipeline(
                        video_path,
                        language,
                    )

                st.session_state["video_result"] = result
                st.session_state["rag_chain"] = result["rag_chain"]
                st.session_state["video_source"] = uploaded_video.name

                st.success("Video analysis completed successfully!")

            except Exception as e:
                st.error(f"Video analysis failed: {e}")

    # -------------------------------------------------------
    # Display Analysis Results
    # -------------------------------------------------------

    if "video_result" in st.session_state:

        result = st.session_state["video_result"]

        st.markdown("---")
        st.header("📊 Video Analysis Results")

        tab_summary, tab_transcript, tab_chat = st.tabs(
            [
                "📋 Summary",
                "📄 Transcript",
                "💬 Chat with Video",
            ]
        )

        # ---------------- Summary ----------------

        with tab_summary:

            st.subheader("📝 Summary")
            st.write(result.get("summary", "No summary available."))

            st.divider()

            st.subheader("✅ Action Items")
            st.write(
                result.get("action_items", "No action items found.")
            )

            st.divider()

            st.subheader("🔑 Key Decisions")
            st.write(
                result.get("key_decisions", "No key decisions found.")
            )

            st.divider()

            st.subheader("❓ Open Questions")
            st.write(
                result.get("open_questions", "No open questions found.")
            )

        # ---------------- Transcript ----------------

        with tab_transcript:

            st.subheader("🎙 Video Transcript")

            st.text_area(
                "Transcript",
                value=result.get("transcript", ""),
                height=450,
                key="video_transcript_display",
            )

        # ---------------- Chat with Video ----------------

        with tab_chat:

            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = []

            # Display previous chat messages
            for message in st.session_state["chat_history"]:

                with st.chat_message(message["role"]):
                    st.write(message["content"])

            question = st.chat_input(
                "Ask anything about the video..."
            )

            if question:

                st.session_state["chat_history"].append(
                    {
                        "role": "user",
                        "content": question,
                    }
                )

                with st.chat_message("user"):
                    st.write(question)

                try:
                    with st.spinner("Finding the answer..."):

                        answer = ask_question(
                            st.session_state["rag_chain"],
                            question,
                        )

                    st.session_state["chat_history"].append(
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )

                    with st.chat_message("assistant"):
                        st.write(answer)

                except Exception as e:
                    st.error(f"Unable to answer the question: {e}")
