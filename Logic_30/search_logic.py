from pytubefix import Search
from backend.config import Settings  # pyright: ignore[reportMissingImports]
from backend.Models_50.requests.search_video_request import SearchVideoRequest
from backend.Models_50.responses.search_video_response import SearchVideoResponseDto, SearchVideoResponse,SearchVideoPagedResponse

def search_for_videos(request: SearchVideoRequest) -> SearchVideoPagedResponse:

    results = Search(request.name)
    while(len(results.videos) < request.page_size):
        results.get_next_results()

    response = SearchVideoPagedResponse()
    for c in results.videos[0:request.page_size]:
        dto = SearchVideoResponseDto()
        dto.name = c.title
        dto.url = c.watch_url
        response.data.append(dto)

    response.success = True
    response.page_size = len(response.data)
    response.page_number = None
    return response
