"""
Transcribe all videos in input_folder_path using AssemblyAI
Uses ASSEMBLYAI_API_KEY in .env file
"""
import os
from pathlib import Path

import assemblyai as aai
from dotenv import load_dotenv
from rich import print

load_dotenv()
aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]

input_folder_path = "../data/audio"
output_folder_path = "../data/transcripts"

input_folder = Path(input_folder_path)
output_folder = Path(output_folder_path)

# Configure AssemblyAI
config = aai.TranscriptionConfig(
    language_code="en",
    word_boost=["streamlit"],
    boost_param="high",
)
transcriber = aai.Transcriber(config=config)

# Transrive each video with AssemblyAI
for video in input_folder.glob("*.mp3"):
    print(f"Transcribing {video.stem}")

    transcript = transcriber.transcribe(str(video))

    # Prefixing filename with `r-` because I'm getting escaping problems in GraphQL on Windows with Verba
    with open(output_folder / f"r-{video.stem}.txt", "w", encoding="utf-8") as f:
        f.writelines([f"{sentence.text}\n" for sentence in transcript.get_sentences()])

    print(f"Transcribed {video.stem}")
