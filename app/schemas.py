from pydantic import BaseModel, HttpUrl

class URLBase(BaseModel):
    url: HttpUrl

class URLCreate(URLBase):
    pass

class URLInfo(URLBase):
    short_code: str
    original_url: HttpUrl

    class Config:
        orm_mode = True
