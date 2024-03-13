from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.transaction import transaction_schema, transaction_crud
from domain.book import book_crud, book_schema
from domain.user.login import get_current_user
from models import Transaction, User
router = APIRouter(
    prefix="/transaction",
)

# 거래 글 전체 조회 함수
@router.get("/", response_model=list[transaction_schema.Transaction])
def transaction_list(db: Session = Depends(get_db)):
    _transaction_list = transaction_crud.get_transaction_list(db)
    return _transaction_list

# 거래 글 등록 함수
@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def transaction_create(_transaction_create: transaction_schema.TransactionCreate,
                    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction_crud.create_transaction(db=db, transaction_create=_transaction_create, user=current_user)

# 거래 글 책조회(isbn) 함수
@router.get("/book/{book_isbn}", response_model=book_schema.Book)
def transaction_book_detail(book_isbn: int, db: Session = Depends(get_db)):
    transaction_book = book_crud.get_book_isbn(db, book_isbn = book_isbn)
    if not transaction_book:
        transaction_api_book = book_crud.search_isbn(db, isbn = book_isbn)
        if transaction_api_book.title != 'None':
            return transaction_api_book
        else:
            raise HTTPException(status_code=404, detail="이 isbn으로 등록된 책이 없습니다. 책을 등록시켜주시길 바랍니다.")
    else:
        return transaction_book

# 거래 글 책등록 함수
@router.post("/book", status_code=status.HTTP_204_NO_CONTENT)
def transaction_book_create(_transaction_book_create: book_schema.BookCreate,
                            db: Session = Depends(get_db)):
    book_crud.create_book(db=db, book_create=_transaction_book_create)

# 거래 글 세부 조회 함수
@router.get("/{transaction_id}", response_model=transaction_schema.Transaction)
def transaction_detail(transaction_id: int, db: Session = Depends(get_db)):
    transaction = transaction_crud.get_transaction(db, transaction_id = transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="transaction not found")
    else:
        return transaction
    

    
# 거래 글 수정 함수
@router.put("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def transaction_update(_transaction_update: transaction_schema.TransactionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_transaction = transaction_crud.get_transaction(db, transaction_id=_transaction_update.transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다.")
    
    if current_user.id != db_transaction.user.id :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다.")
        
    transaction_crud.update_transaction(db=db, db_transaction=db_transaction, transaction_update=_transaction_update)


