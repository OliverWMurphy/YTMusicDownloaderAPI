from pytubefix import Search

from backend.config import Settings  # pyright: ignore[reportMissingImports]
from backend.Models_50.requests.search_video_request import SearchVideoRequest
from backend.Models_50.responses.search_video_response import SearchVideoResponse,SearchVideoPagedResponse

def search_for_videos(request: SearchVideoPagedResponse) -> SearchVideoPagedResponse:
    results = Search(request.name)
    response = SearchVideoPagedResponse()

    for c in results.videos:
        data = SearchVideoResponse()
        data.name = c.title
        data.url = c.watch_url
        response.data.append(data)

    response.success = True
    return response
