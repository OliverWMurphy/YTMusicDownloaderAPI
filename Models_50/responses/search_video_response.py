from backend.Models_50.core import base_response


class SearchVideoResponse(base_response.BaseResponse):
    name: str | None = None
    url: str | None = None
    video_length: int |  None = None

class SearchVideoPagedResponse(base_response.BasePagedResponse):
    data: list[SearchVideoResponse] = []
