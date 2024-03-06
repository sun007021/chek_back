from datetime import datetime
from models import Transaction
from sqlalchemy.orm import Session
from domain.transaction.transaction_schema import TransactionCreate

# 책 전체 조회 함수
def get_transaction_list(db: Session):
    transaction_list = db.query(Transaction)\
        .order_by(Transaction.id.asc())\
        .all()
    return transaction_list

# 거래 글 등록 함수
def create_transaction(db: Session, transaction_create: TransactionCreate):
    db_transaction = Transaction( 
                    subject=transaction_create.subject,
                    content=transaction_create.content,
                    title=transaction_create.title,
                    author=transaction_create.author,
                    isbn=transaction_create.isbn,
                    publisher=transaction_create.publisher,
                    publicationdate=transaction_create.publicationdate,
                    image=transaction_create.image,
                    create_date=datetime.now())
    db.add(db_transaction)
    db.commit()
