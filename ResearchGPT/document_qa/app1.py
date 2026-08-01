import os
import shutil
import gc
import streamlit as st

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


def run():
    st.set_page_config(
        page_title="PDF RAG Chatbot",
        page_icon="📚",
        layout="wide"
    )

    st.title("📚 PDF RAG Chatbot")

    UPLOAD_FOLDER = "uploads"
    DB_FOLDER = "chroma_db"

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    embedding_model = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    llm = ChatMistralAI(
        model="mistral-small-2506"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a helpful AI assistant.

Answer ONLY using the given context.

If the answer is not available in the context, reply:

Answer is not present in document.
"""
            ),
            (
                "human",
                """
Context:
{context}

Question:
{question}
"""
            )
        ]
    )

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    if uploaded_file:

        pdf_path = os.path.join(
            UPLOAD_FOLDER,
            uploaded_file.name
        )

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("Create Knowledge Base"):

            if "vector_store" in st.session_state:
                del st.session_state["vector_store"]

            gc.collect()

            if os.path.exists(DB_FOLDER):
                shutil.rmtree(DB_FOLDER, ignore_errors=True)

            loader = PyPDFLoader(pdf_path)
            docs = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.split_documents(docs)

            Chroma.from_documents(
                documents=chunks,
                embedding=embedding_model,
                persist_directory=DB_FOLDER
            )

            st.session_state["vector_store"] = Chroma(
                persist_directory=DB_FOLDER,
                embedding_function=embedding_model
            )

            st.success("Knowledge Base Created Successfully!")

    if "vector_store" not in st.session_state:
        if os.path.exists(DB_FOLDER):
            st.session_state["vector_store"] = Chroma(
                persist_directory=DB_FOLDER,
                embedding_function=embedding_model
            )

    if "vector_store" in st.session_state:

        retriever = st.session_state["vector_store"].as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 4,
                "fetch_k": 10,
                "lambda_mult": 0.5
            }
        )

        question = st.chat_input("Ask a question about the PDF")

        if question:

            with st.chat_message("user"):
                st.write(question)

            docs = retriever.invoke(question)

            context = "\n\n".join(
                doc.page_content for doc in docs
            )

            final_prompt = prompt.invoke(
                {
                    "context": context,
                    "question": question
                }
            )

            response = llm.invoke(final_prompt)

            with st.chat_message("assistant"):
                st.write(response.content)