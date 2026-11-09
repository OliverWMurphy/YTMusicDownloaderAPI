from backend.Models_50.core import base_response
from pydantic import BaseModel as _BaseModel


class SearchVideoResponseDto(_BaseModel):
    name: str | None = None
    url: str | None = None
    video_length: int |  None = None

class SearchVideoResponse(base_response.BaseResponse):
    data: SearchVideoResponseDto | None = None

class SearchVideoPagedResponse(base_response.BasePagedResponse):
    data: list[SearchVideoResponseDto] = []
