from datetime import datetime
from domain.book.book_schema import BookCreate, BookUpdate
from models import Book
from sqlalchemy.orm import Session
import requests
from bs4 import BeautifulSoup as BS

api_link = 'https://openapi.naver.com/v1/search/book_adv.xml'

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

# 책 isbn으로 조회 함수
def get_book_isbn(db: Session, book_isbn: int):
    book= db.query(Book).filter(Book.isbn == book_isbn).first()
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

# 책 삭제 함수
def delete_book(db: Session, db_book: Book):
    db.delete(db_book)
    db.commit()

# 네이버에서 책 isbn으로 크롤링
def search_isbn(db: Session, isbn : int):
    headers = {"X-Naver-Client-Id": "O2CToPmdUnCPeO4FArtC", "X-Naver-Client-Secret": "4KWdzrDnTF"}
    isbn_api_link = api_link + "?d_isbn=" + str(isbn)
    res = requests.get(isbn_api_link, headers = headers) 
    text = res.text

    book = BS(text,'html.parser')
    book_titles = book.select('title')
    
    if  len(book_titles) > 1:
        db_book = Book( title=book.select('title')[1].text,
                        author=book.select('author')[0].text,
                        isbn= isbn,
                        publisher=book.select('publisher')[0].text,
                        publicationdate=book.select('pubdate')[0].text,
                        image= "None")
        db.add(db_book)
        db.commit()
        return db_book
    else:
        db_book = Book( title="None",
                        author="None",
                        isbn= isbn,
                        publisher="None",
                        publicationdate="None",
                        image= "None")
        return db_book