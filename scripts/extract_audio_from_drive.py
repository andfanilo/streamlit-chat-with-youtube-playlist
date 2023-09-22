"""
Browse input folder for all videos, extract audio as mp3 and copy to output folder
"""
import subprocess
from pathlib import Path

from rich import print

input_folder_path = "D:/XXX"
output_folder_path = "../data/audio"

input_folder = Path(input_folder_path)
output_folder = Path(output_folder_path)

# I'm using the following tree structure for my videos
#
# ├── 2022 Q1
# │   ├── stlite
# |   |   └── stlite.mp4
# │   └── st-css
# |       └── st-css.mp4
# └── 2022 Q2
#     ├── components-tutorial
#     |   └── components-tutorial.mp4
#     └── vlog_202305
#         └── vlog_202305.mp4

# Keep folders `Qx 2022` or `Qx 2023`
root_folders = [
    folder
    for folder in input_folder.iterdir()
    if ("2022" in folder.name or "2023" in folder.name) and folder.is_dir()
]

# Retrieve all project folders
video_folders = [
    video_folder for folder in root_folders for video_folder in folder.iterdir()
]

# Browse through projects, convert videos to audio
for video_folder in video_folders:
    folder_name = video_folder.stem
    video_file = video_folder / f"{folder_name}.mp4"

    if not video_file.exists():
        print(
            f"[bold red]Problem with folder {video_folder.stem}, skipping...[/bold red]"
        )
        continue

    ffmpeg_cmd = f'ffmpeg -i "{video_file}" "{output_folder / video_folder.stem}.mp3"'
    print(f"Processing {video_folder.stem}; will run command '{ffmpeg_cmd}'")
    subprocess.call(ffmpeg_cmd, shell=True)
    print(f"Processed {video_folder.stem}")
