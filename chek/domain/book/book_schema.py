import datetime
from fastapi import HTTPException
from pydantic import BaseModel, validator

# 책 전체조회할때 쓰는 객체
class Book(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    publisher: str
    publicationdate: str
    image: str

# 책 등록할때 쓰는 객체
class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    publisher: str
    publicationdate: str
    image: str | None= None

    # request에 빈칸이 있는 경우 예외처리 함수
    @validator('title', 'author', 'isbn', 'publisher', 'publicationdate')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise HTTPException(status_code=400, detail="빈 값은 허용되지 않습니다.")
        return v

# 책 수정할때 쓰는 객체
class BookUpdate(BookCreate):
   book_id: int
