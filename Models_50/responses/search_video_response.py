from backend.Models_50.core import base_response


class SearchVideoResponse(base_response.BaseResponse):
    name: str
    url: str
    video_length: int

class SearchVideoPagedResponse(base_response.BasePagedResponse):
    data: list[SearchVideoResponse] | None = None
