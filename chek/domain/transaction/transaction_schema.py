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

# 거래 글 등록할때 쓰는 객체
class TransactionCreate(BaseModel):
    subject: str
    content: str
    title: str
    author: str
    isbn: str
    publisher: str
    publicationdate: str
    image: str

    # request에 빈칸이 있는 경우 예외처리 함수
    @validator('subject','content','title', 'author', 'isbn', 'publisher', 'publicationdate')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise HTTPException(status_code=400, detail="빈 값은 허용되지 않습니다.")
        return v

# # 거래 글 수정할때 쓰는 객체
# class TransactionUpdate(TransactionCreate):
#     transaction_id: int