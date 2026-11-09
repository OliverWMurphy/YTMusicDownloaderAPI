from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from backend import config
from backend.Logic_30 import search_logic
from backend.Models_50.requests.search_video_request import SearchVideoRequest
from backend.Models_50.responses.search_video_response import SearchVideoPagedResponse

router = APIRouter(
    prefix="/search",
    tags=["search"],
)
RunSettings = Annotated[config.Settings, Depends(config.get_settings)]



@router.get("/test")
async def test(settings: RunSettings) -> SearchVideoPagedResponse:
    print (settings)
    return await list_videos(settings, SearchVideoRequest())

@router.post("/videos")
async def list_videos(settings: RunSettings,
                        request: SearchVideoRequest ) -> SearchVideoPagedResponse:

    return search_logic.search_for_videos(request)
