from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from backend import config
from backend.Logic_30 import download_logic, processing_logic

router = APIRouter(
    prefix="/video",
    tags=["video"],
)

RunSettings = Annotated[config.Settings, Depends(config.get_settings)]


@router.get("/test")
async def test(settings: RunSettings):
    print (settings)
    return await download_single(settings,"1bsFH6t8eFw")

#splitTracks: Union[bool, None]
@router.get("/single/{videoId}")
async def download_single(settings: RunSettings ,videoId: str
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
