import whisper
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None


def load_model():

    global _model

    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL} ...")

        _model = whisper.load_model(WHISPER_MODEL)

        print("Whisper model loaded.")

    return _model


def transcribe_chunk(chunk_path: str, language: str = None) -> str:

    model = load_model()

    if language:
        result = model.transcribe(
            chunk_path,
            language=language,
            task="transcribe"
        )
    else:
        result = model.transcribe(
            chunk_path,
            task="transcribe"
        )

    return result["text"]


def transcribe_all(chunks: list, language: str = None) -> str:

    full_transcript = ""

    print("Using Whisper for transcription...")

    for i, chunk in enumerate(chunks):

        print(f"Transcribing chunk {i+1}/{len(chunks)}...")

        text = transcribe_chunk(chunk, language)

        full_transcript += text + " "

    print("Transcription complete.")

    return full_transcript.strip()