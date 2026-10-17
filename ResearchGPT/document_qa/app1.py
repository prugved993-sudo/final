import os
import shutil
import tempfile

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def process_pdf(uploaded_file):
    """Process any PDF uploaded by the user."""

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".pdf"
    ) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        pdf_path = temp_file.name

    try:
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        if not docs or not any(doc.page_content.strip() for doc in docs):
            raise ValueError("No readable text found in this PDF.")

        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        chunks = splitter.split_documents(docs)

        # Generate embeddings
        embedding_model = get_embedding_model()

        # Create a unique temporary database for this upload
        db_folder = tempfile.mkdtemp(prefix="researchgpt_chroma_")

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory=db_folder,
            collection_name="researchgpt_documents",
        )

        return vector_store, db_folder

    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


# Streamlit upload interface
st.subheader("📚 PDF RAG Chatbot")

uploaded_file = st.file_uploader(
    "Upload any PDF",
    type=["pdf"],
)

if uploaded_file is not None:
    if st.button("Process PDF"):
        with st.spinner("Processing your PDF..."):
            try:
                vector_store, db_folder = process_pdf(uploaded_file)

                st.session_state["vector_store"] = vector_store
                st.session_state["db_folder"] = db_folder
                st.session_state["pdf_name"] = uploaded_file.name

                st.success(f"Processed: {uploaded_file.name}")

            except Exception as e:
                st.error(f"PDF processing failed: {e}")

if "vector_store" in st.session_state:
    question = st.text_input("Ask a question about your PDF")

    if st.button("Get Answer") and question.strip():
        with st.spinner("Finding an answer..."):
            try:
                results = st.session_state["vector_store"].similarity_search(
                    question,
                    k=4,
                )

                context = "\n\n".join(
                    doc.page_content for doc in results
                )

                st.write("**Relevant PDF content:**")
                st.write(context)

            except Exception as e:
                st.error(f"Search failed: {e}")
