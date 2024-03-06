from datetime import datetime
from models import Transaction
from sqlalchemy.orm import Session

# 책 전체 조회 함수
def get_transaction_list(db: Session):
    transaction_list = db.query(Transaction)\
        .order_by(Transaction.id.asc())\
        .all()
    return transaction_list