from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.book import book_schema, book_crud
from domain.user.login import get_current_user 
from models import User

router = APIRouter(
    prefix="/book",
)

# 책 전체 조회 함수
@router.get("/", response_model=list[book_schema.Book])
def book_list(db: Session = Depends(get_db)):
    _book_list = book_crud.get_book_list(db)
    return _book_list

# 책 등록 함수
@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def book_create(_book_create: book_schema.BookCreate,
                    db: Session = Depends(get_db)):
    book_crud.create_book(db=db, book_create=_book_create)


# 책 세부 조회 함수
@router.get("/{book_id}", response_model=book_schema.Book)
def book_detail(book_id: int, db: Session = Depends(get_db)):
    book = book_crud.get_book(db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return book
    
# 책 수정 함수
@router.put("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def book_update(_book_update: book_schema.BookUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = book_crud.get_book(db, book_id=_book_update.book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다.")
    
    if current_user.is_superuser != True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다.")
    
    book_crud.update_book(db=db, db_book=db_book, book_update=_book_update)

# 책 삭제 함수
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def book_delete(_book_delete: book_schema.BookDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_book = book_crud.get_book(db, book_id=_book_delete.book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다.")
    
    if current_user.is_superuser != True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다.")
    
    book_crud.delete_book(db=db, db_book=db_book)