import datetime

from pydantic import BaseModel, validator


class Book(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    publisher: str
    publicationdate: str
    image: str

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    publisher: str
    publicationdate: str
    image: str | None= None

    @validator('title', 'author', 'isbn', 'publisher', 'publicationdate')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v