from pydantic import BaseModel as _BaseModel
from typing import Annotated, TypeVar
T = TypeVar('T')


class BaseResponse(_BaseModel):
    data: T | None = None
    success: bool = False

class BasePagedResponse(_BaseModel):
    page_size: int = -1
    page_number: int = -1
    data: list
    success: bool = False
