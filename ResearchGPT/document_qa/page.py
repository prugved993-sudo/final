from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate

url = "https://www.lenovo.com/in/en/c/laptops/thinkpad/?orgRef=https%253A%252F%252Fwww.bing.com%252F&msockid=01b91b2e1b186949052a0daf1a8368fa"
data = WebBaseLoader(url)

docs = data.load()
print(docs[0].page_content)