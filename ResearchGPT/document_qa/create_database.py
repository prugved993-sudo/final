from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# Load the text document
loader = PyPDFLoader("OSY.pdf")
docs = loader.load()


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)



chunks = splitter.create_documents(
    [doc.page_content for doc in docs]
)




embedding_model = OllamaEmbeddings(model="nomic-embed-text")

vector_store = Chroma.from_documents(
    documents = chunks,
    embedding = embedding_model,
    persist_directory="chroma_db"
)


