import os
import shutil
import subprocess
from pathlib import Path

from pytubefix import Chapter, Stream

from backend.config import Settings  # pyright: ignore[reportMissingImports]


def create_blob_path(video_id:str, settings: Settings) -> Path:
    return Path(settings.storage_url).joinpath(video_id)


def process_audio(audio: Stream,
                   fileDestination: Path,
                   extension: str = ".mp3") -> Path:
    audioName = Path(audio.default_filename)

    mp3File = audioName.with_suffix(extension)
    print("Starting FFMPEG")
    print(f"{fileDestination}/{audio.default_filename} -> {fileDestination}/{mp3File}")

    subprocess.run(
        ["ffmpeg", "-i",
         fileDestination/audio.default_filename,
           fileDestination/mp3File],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        check= True
    )
    print("Ending FFMPEG")

    return fileDestination/mp3File

def splitAudio(audioName: str, chapters: list[Chapter]) -> str:
    folderName = os.path.splitext(audioName)[0]
    folderExists = False
    print(folderName)
    while not folderExists:
        try:
            Path.mkdir(folderName)
            folderExists = True
        except FileExistsError:
            folderName += "Copy"

    for chapter in chapters:
        name = f"{chapter.title}.mp3"
        startTime = f"{chapter.start_seconds}"
        duration = f"{chapter.duration}"

        ffmpeg = ["ffmpeg",
         "-ss", startTime, "-t", duration, "-i", audioName, f"{folderName}/{name}"]
        print(f"Running {ffmpeg}" )
        subprocess.run(
            ffmpeg,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            check= True
        )

    zipName = shutil.make_archive(folderName, 'zip', folderName)
    shutil.rmtree(folderName)
    return zipName

