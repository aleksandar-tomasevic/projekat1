from pydantic import BaseModel

class PostCreate(BaseModel):
    user_id: int
    title: str
    body: str

class PostPatch(BaseModel):
    user_id: int | None = None
    title: str | None = None
    body: str | None = None
