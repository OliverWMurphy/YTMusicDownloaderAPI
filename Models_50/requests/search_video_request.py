from backend.Models_50.core import base_request


class SearchVideoRequest(base_request.BasePagedRequest):
    name: str
