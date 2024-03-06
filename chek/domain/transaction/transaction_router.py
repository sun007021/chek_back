from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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