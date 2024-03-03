from datetime import datetime

from domain.book.book_schema import BookCreate
from models import Book
from sqlalchemy.orm import Session


def get_book_list(db: Session):
    book_list = db.query(Book)\
        .order_by(Book.id.asc())\
        .all()
    return book_list
    
def create_book(db: Session, book_create: BookCreate):
    db_book = Book( title=book_create.title,
                    author=book_create.author,
                    isbn=book_create.isbn,
                    publisher=book_create.publisher,
                    publicationdate=book_create.publicationdate,
                    image=book_create.image)
    db.add(db_book)
    db.commit()