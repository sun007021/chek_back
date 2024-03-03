import os
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt, JWTError
from dotenv import load_dotenv

from domain.user.user_crud import pwd_context, get_user


class Settings():
    load_dotenv()
    ACCESS_TOKEN_EXPIRE_MINUTES: int  = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

settings = Settings()

#login시 pw일치 여부와 jwt 토큰 발급
def login(db: Session, form_data: OAuth2PasswordRequestForm = Depends()):
    # check user and password
    user = get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.username,
        "is_superuser": user.is_superuser,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "is_superuser": user.is_superuser
    }
