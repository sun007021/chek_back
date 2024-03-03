from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email,
                   university_id=user_create.university_id
                   )
    db.add(db_user)
    db.commit()

# get user from username or email that already exists
def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()

def register(db: Session, user_create: UserCreate):
    user = get_existing_user(db, user_create)
    if user:
        raise HTTPException(status_code=409, detail='이미 존재하는 사용자입니다.')
    create_user(db, user_create)
    return True

def get_users(db: Session):
    user_list = db.query(User).all()
    return user_list

def get_user(db: Session, username: int):
    user = db.query(User).filter(User.username == username).first()
    return user