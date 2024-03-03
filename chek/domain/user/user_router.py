from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema

router = APIRouter(
    prefix="/user",
)


@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user_crud.create_user(db=db, user_create=_user_create)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[user_schema.UserList])
def user_list(db: Session = Depends(get_db)):
    _user_list = user_crud.get_users(db=db)
    return _user_list