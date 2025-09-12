from pydantic import BaseModel
from app.schemas.author import AuthorResponse

class BookAuthorResponse(BaseModel):
    author: AuthorResponse

    class Config:
        from_attributes = True