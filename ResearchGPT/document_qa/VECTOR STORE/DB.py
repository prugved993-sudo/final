from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv


load_dotenv()

from langchain_core.documents import Document


docs = [
    Document(
        page_content="Python is a popular programming language.",
        metadata={"source": "python.pdf", "page": 1}
    ),

    Document(
        page_content="Machine Learning learns patterns from data.",
        metadata={"source": "ml.pdf", "page": 2}
    ),

    Document(
        page_content="LangChain helps build RAG applications.",
        metadata={"source": "langchain.pdf", "page": 3}
    )
]




embedding_model = OllamaEmbeddings(model="nomic-embed-text")

vector_store = Chroma.from_documents(
    documents = docs,
    embedding = embedding_model,
    persist_directory="chroma_db"
)


result = vector_store.similarity_search("Who is learns patterns from data?",k=2)

for r in result:
    print(r)
