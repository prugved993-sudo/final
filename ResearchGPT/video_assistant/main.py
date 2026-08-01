from dotenv import load_dotenv

from .utils.audio_processor import process_input
from .core.transcriber import transcribe_all
from .core.summarizer import summarize
from .core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from .core.rag_engine import (
    build_rag_chain,
    ask_question,
)

load_dotenv()


def run_pipeline(source: str, language: str = "english") -> dict:
    print("Starting AI Video Assistant")

    # Process input (download/convert/chunk audio)
    chunks = process_input(source)

    # Transcribe audio
    transcript = transcribe_all(chunks, language=language)

    # Generate summary and extract information
    summary = summarize(transcript)
    action_items = extract_action_items(transcript)
    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)

    # Build RAG pipeline
    rag_chain = build_rag_chain(transcript)

    return {
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }


if __name__ == "__main__":
    # CLI Entry Point
    source = input("Enter YouTube URL or local file path: ").strip()
    language = input("Language (english/hinglish): ").strip() or "english"

    result = run_pipeline(source, language)

    print("\n" + "=" * 60)
    print("\n📋 Summary:")
    print(result["summary"])

    print("\n✅ Action Items:")
    print(result["action_items"])

    print("\n🔑 Key Decisions:")
    print(result["key_decisions"])

    print("\n❓ Open Questions:")
    print(result["open_questions"])

    print("=" * 60)

    # Chat with transcript using RAG
    print("\n💬 Chat with your meeting (type 'exit' to quit)\n")

    rag_chain = result["rag_chain"]

    while True:
        question = input("You: ").strip()

        if question.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break

        if not question:
            continue

        answer = ask_question(rag_chain, question)
        print(f"\n🤖 Assistant: {answer}\n")