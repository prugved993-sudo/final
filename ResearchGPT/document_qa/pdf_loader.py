
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate

from langchain_text_splitters import TokenTextSplitter

# Load environment variables (.env)
load_dotenv()

# Load the text document
loader = PyPDFLoader("OSY.pdf")
docs = loader.load()


splitter = TokenTextSplitter(chunk_size=100,chunk_overlap=10)

chunks = splitter.split_documents(docs)
print(len(chunks))


# Create the prompt template
'''template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant that summarizes the given text in a concise way."),
    ("human", "{data}")
])

# Initialize the Mistral model
model = ChatMistralAI(
    model="mistral-small-2506"
)

# Format the prompt with the document content
prompt = template.format_messages(
    data=docs[0].page_content
)

# Send the prompt to the model
result = model.invoke(prompt)

# Print the summary
print(result.content)'''



