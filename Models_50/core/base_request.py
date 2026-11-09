from pydantic import BaseModel as _BaseModel


# Not sure if I need any common request just yet.
class BaseRequest(_BaseModel):
    pass

class BasePagedRequest(_BaseModel):
    page_size: int
    page_number: int

