"""
Download/extract audio as mp3 from all Youtube videos in a playlist 
"""
from pathlib import Path

import yt_dlp
from rich import print

output_folder_path = "../data/audio"
output_folder = Path(output_folder_path)

playlist_to_download_url = (
    "https://www.youtube.com/playlist?list=PLJJOI_ZUeaBpO7r3GrvYi2KeVhS1Vjerc"
)

# Define download options to extract audio as mp3 for each video + file name 
ydl_opts = {
    "extract_audio": True,
    "format": "bestaudio",
    "outtmpl": str(output_folder / "%(title)s"),
    # "ratelimit": 50000, # <--- Uncomment to rate limit for large playlists
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }
    ],
}

# Download all videos
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(playlist_to_download_url, download=True)
    video_title = info_dict["title"]
    print(f"[bold yellow]Downloading {video_title}[/bold yellow]")
    error_code = ydl.download(playlist_to_download_url)
