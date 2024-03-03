from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.book import book_schema, book_crud

router = APIRouter(
    prefix="/book",
)


@router.get("/", response_model=list[book_schema.Book])
def book_list(db: Session = Depends(get_db)):
    _book_list = book_crud.get_book_list(db)
    return _book_list

@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def book_create(_book_create: book_schema.BookCreate,
                    db: Session = Depends(get_db)):
    book_crud.create_book(db=db, book_create=_book_create)

@router.get("/{book_id}", response_model=book_schema.Book)
def book_detail(book_id: int, db: Session = Depends(get_db)):
    book = book_crud.get_book(db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return book