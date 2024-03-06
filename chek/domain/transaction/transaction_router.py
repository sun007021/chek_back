from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.transaction import transaction_schema, transaction_crud

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
                    db: Session = Depends(get_db)):
    transaction_crud.create_transaction(db=db, transaction_create=_transaction_create)
