import os
import wave
import yt_dlp
import subprocess
import streamlit as st

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:

    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "quiet": False,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "geo_bypass": True,
        "postprocessors": [ 
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            filename = ydl.prepare_filename(info)

            filename = os.path.splitext(filename)[0] + ".wav"

            if not os.path.exists(filename):
                raise FileNotFoundError(
                    f"Downloaded file not found:\n{filename}"
                )

            return filename

    except Exception as e:

        st.error("❌ YouTube download failed.")

        st.exception(e)

        raise


def convert_to_wav(input_path: str) -> str:

    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    try:

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                input_path,
                "-ac",
                "1",
                "-ar",
                "16000",
                output_path,
            ],
            check=True,
        )

    except Exception as e:
        st.error("❌ FFmpeg conversion failed.")
        st.exception(e)
        raise

    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10):

    chunk_paths = []

    with wave.open(wav_path, "rb") as wf:

        params = wf.getparams()
        frame_rate = wf.getframerate()
        chunk_frames = chunk_minutes * 60 * frame_rate

        index = 0

        while True:

            frames = wf.readframes(chunk_frames)

            if not frames:
                break

            chunk_path = f"{wav_path}_chunk_{index}.wav"

            with wave.open(chunk_path, "wb") as out:
                out.setparams(params)
                out.writeframes(frames)

            chunk_paths.append(chunk_path)
            index += 1

    return chunk_paths


def process_input(source: str):

    if source.startswith(("http://", "https://")):

        st.info("Downloading YouTube audio...")

        wav_path = download_youtube_audio(source)

    else:

        st.info("Converting local file....")

        wav_path = convert_to_wav(source)

    st.info("Chunking audio...")

    chunks = chunk_audio(wav_path)

    st.success(f"Created {len(chunks)} audio chunks.")

    return chunks
