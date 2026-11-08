
from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pytubefix.exceptions import VideoUnavailable

from . import config
from .logic import download_logic, processing_logic

background_tasks = BackgroundTasks()
app = FastAPI()

@lru_cache
def get_settings():
    return config.Settings()

@app.exception_handler(VideoUnavailable)
async def VideoUnavailable_exception_handler(request: Request, ex: VideoUnavailable):
    return JSONResponse(
        status_code=500,
        content={"message": f"Can not get video. {ex.error_string}"},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allow all origins, change to specific origins for security (e.g., ["http://localhost:5500"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/heartbeat")
async def root(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {"message": "I'm alive!",
             "author": settings.creator,
             "fullSettings": settings,
             "Path": list(Path("./blobs").iterdir())}

@app.get("/test")
async def test(settings: Annotated[config.Settings, Depends(get_settings)]):
    return await download_single(settings,"1bsFH6t8eFw")

#splitTracks: Union[bool, None]
@app.get("/api/single/{videoId}")
async def download_single(settings: Annotated[config.Settings, Depends(get_settings)]
                          ,videoId: str
                          , splitTracksFromChapters: bool = False):


    video = await download_logic.getVideo(videoId)
    blob_path = processing_logic.create_blob_path(video.video_id, settings)
    audio = await download_logic.getAudio(video,blob_path)
    print("audioName",audio.default_filename)
    targetLocation = processing_logic.process_audio(audio,blob_path)


    print("targetLocation",targetLocation)
    if splitTracksFromChapters:
        print("Splitting")
        chapters = video.chapters
        targetLocation = processing_logic.splitAudio(targetLocation,chapters)

    print("About to download")
    # Use FileResponse to return the file, with headers to prompt download
    return FileResponse(
        path=targetLocation,
        media_type="video/mp4",
        filename=targetLocation.name,  # This sets the name of the file for download
    )
