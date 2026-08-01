import streamlit as st

from deep_research.pipeline import run_research_pipeline


def run():
    st.title("🤖 Multi-Agent Research Assistant")

    st.markdown("""
Generate a detailed research report using a **Multi-Agent AI System**.

This application uses:
- 🔎 Search Agent
- 📖 Reader Agent
- ✍️ Writer Chain
- ⭐ Critic Chain
""")

    st.divider()

    topic = st.text_input(
        "Enter a Research Topic",
        placeholder="Example: Artificial Intelligence in Healthcare",
        key="research_topic"
    )

    if st.button("🚀 Generate Report", use_container_width=True, key="generate_report"):

        if not topic.strip():
            st.warning("Please enter a research topic.")
            return

        with st.spinner("Research agents are working... Please wait..."):

            try:
                result = run_research_pipeline(topic)

                st.success("Research completed successfully!")

                tab1, tab2, tab3 = st.tabs(
                    ["📄 Report", "⭐ Critic Feedback", "📚 Research Data"]
                )

                with tab1:
                    st.subheader("Research Report")
                    st.markdown(result["report"])

                with tab2:
                    st.subheader("Critic Feedback")
                    st.markdown(result["feedback"])

                with tab3:
                    st.subheader("Search Results")

                    with st.expander("View Search Results"):
                        st.text(result["search_result"])

                    st.subheader("Scraped Content")

                    with st.expander("View Scraped Content"):
                        st.text(result["scrapped_content"])

            except Exception as e:
                st.error("An error occurred while running the research pipeline.")
                st.exception(e)