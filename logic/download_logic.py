
from pathlib import Path
from urllib.error import HTTPError

from fastapi import HTTPException
from pytubefix import YouTube as YT
from pytubefix.streams import Stream


async def getVideo(vid_id: str)  -> YT:

    video = YT(id_to_URL(vid_id))
    video.check_availability()
    return video

async def getAudio(video: YT, path: Path)  -> Stream:
    audio = video.streams.get_audio_only()

    if audio is None:
        raise  HTTPException(status_code=500,
                            detail="Can not get audio stream")
    try:
        audio.download(path)
        print("Download Successful!")
    except HTTPError:
        print("Could get audio stream, but download failed")
        raise HTTPException(status_code=500,
                            detail="Could get audio stream, but download failed")

    return audio

def id_to_URL(vid_id: str)-> str:
    return "https://www.youtube.com/watch?v=" + vid_id
