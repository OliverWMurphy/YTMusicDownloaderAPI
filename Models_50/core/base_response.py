from pydantic import BaseModel as _BaseModel


class BaseResponse(_BaseModel):
    data: dict | None = None
    success: bool = False

class BasePagedResponse(_BaseModel):
    page_size: int = -1
    page_number: int = -1
    data: list
    success: bool = False
