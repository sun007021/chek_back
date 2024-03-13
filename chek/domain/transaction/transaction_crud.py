from datetime import datetime
from models import Transaction, User
from sqlalchemy.orm import Session
from domain.transaction.transaction_schema import TransactionCreate, TransactionUpdate

# 거래 글 전체 조회 함수
def get_transaction_list(db: Session):
    transaction_list = db.query(Transaction)\
        .order_by(Transaction.id.asc())\
        .all()
    return transaction_list

# 거래 글 등록 함수
def create_transaction(db: Session, transaction_create: TransactionCreate, user: User):
    db_transaction = Transaction( 
                    subject=transaction_create.subject,
                    content=transaction_create.content,
                    isbn=transaction_create.isbn,
                    image=transaction_create.image,
                    create_date=datetime.now(),
                    user=user
                    )
    db.add(db_transaction)
    db.commit()



# 거래 글 세부 조회 함수
def get_transaction(db: Session, transaction_id: int):
    transaction = db.query(Transaction).get(transaction_id)

    return transaction

# 거래 글 수정 함수
def update_transaction(db: Session, db_transaction: Transaction, transaction_update: TransactionUpdate):
    db_transaction.subject = transaction_update.subject
    db_transaction.content = transaction_update.content
    db_transaction.isbn = transaction_update.isbn
    db_transaction.image = transaction_update.image
    db_transaction.modify_date = datetime.now()
    db.add(db_transaction)
    db.commit()
