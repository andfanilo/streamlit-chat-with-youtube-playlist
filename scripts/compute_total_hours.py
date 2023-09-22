"""
Compute total length duration for all mp3s in input_folder_path
Helpful to estimate AssemblyAI Async Transcription cost
"""
from pathlib import Path

from mutagen.mp3 import MP3
from rich import print
from rich.panel import Panel

input_folder_path = "../data/audio"

input_folder = Path(input_folder_path)
total_length = 0

# Browse each mp3 file for its length
for audio_file in input_folder.glob("*.mp3"):
    audio = MP3(audio_file)
    audio_length = audio.info.length
    total_length += audio_length
    print(f"Length of '{audio_file.stem}': {(audio_length / 60):.2f} minutes")

# Print total length
print(
    Panel.fit(
        f"""Total Length: {(total_length / 60 / 60):.2f} hours
AssemblyAI Async Transcription price: {(0.65 * total_length / 60 / 60):.2f}€"""
    )
)
