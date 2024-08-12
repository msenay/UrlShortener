from pydantic import BaseModel, ConfigDict


class URLBase(BaseModel):
    original_url: str


class URLCreate(URLBase):
    pass


class URL(URLBase):
    id: int
    short_url: str

    model_config = ConfigDict(from_attributes=True)
