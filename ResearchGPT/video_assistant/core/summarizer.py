from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os


def get_llm():
    return ChatMistralAI(
        model="mistral-small-2506",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3
    )


def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200
    )
    return splitter.split_text(transcript)


def summarize(transcript: str) -> str:

    llm = get_llm()

    # -------- Map Step --------
    map_prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize this portion of the meeting concisely."),
        ("human", "{text}")
    ])

    map_chain = map_prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)

    chunk_summaries = []

    for chunk in chunks:
        summary = map_chain.invoke({"text": chunk})
        chunk_summaries.append(summary)

    # -------- Reduce Step --------
    combined_text = "\n\n".join(chunk_summaries)

    combined_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Combine these summaries into one professional meeting summary in bullet points."
        ),
        ("human", "{text}")
    ])

    combined_chain = combined_prompt | llm | StrOutputParser()

    final_summary = combined_chain.invoke({"text": combined_text})

    return final_summary