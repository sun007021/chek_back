from datetime import datetime

from domain.book.book_schema import BookCreate, BookUpdate
from models import Book
from sqlalchemy.orm import Session

# 책 전체 조회 함수
def get_book_list(db: Session):
    book_list = db.query(Book)\
        .order_by(Book.id.asc())\
        .all()
    return book_list

# 책 등록 함수
def create_book(db: Session, book_create: BookCreate):
    db_book = Book( title=book_create.title,
                    author=book_create.author,
                    isbn=book_create.isbn,
                    publisher=book_create.publisher,
                    publicationdate=book_create.publicationdate,
                    image=book_create.image)
    db.add(db_book)
    db.commit()

# 책 세부 조회 함수
def get_book(db: Session, book_id: int):
    book = db.query(Book).get(book_id)

    return book

# 책 수정 함수
def update_book(db: Session, db_book: Book, book_update: BookUpdate):
    db_book.title = book_update.title
    db_book.author = book_update.author
    db_book.isbn = book_update.isbn
    db_book.publisher = book_update.publisher
    db_book.publicationdate = book_update.publicationdate
    db_book.image = book_update.image
    db.add(db_book)
    db.commit()
