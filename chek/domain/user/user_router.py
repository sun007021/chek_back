from datetime import datetime, timedelta
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context
from domain.user.login import login

router = APIRouter(
    prefix="/user",
)

#register
@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user_crud.create_user(db=db, user_create=_user_create)

#get user list
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[user_schema.UserList])
def user_list(db: Session = Depends(get_db)):
    _user_list = user_crud.get_users(db=db)
    return _user_list

#login
@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    access_token = login(db, form_data)
    return access_token