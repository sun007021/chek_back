import datetime
from fastapi import HTTPException
from pydantic import BaseModel, validator

# 거래 글 전체조회할때 쓰는 객체 , book_id는 책 db에 없는 신규책인 경우가 있을 수 있어서  | None = None 
class Transaction(BaseModel):
    id: int
    subject: str
    content: str
    book_id: int | None = None
    title: str
    author: str
    isbn: str
    publisher: str
    publicationdate: str
    image: str
    create_date: datetime.datetime
