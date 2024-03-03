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

def get_users(db: Session):
    user_list = db.query(User).all()
    return user_list