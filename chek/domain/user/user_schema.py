from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo

class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr
    university_id: int | None = None

    @field_validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v


class UserList(BaseModel):
    id: int
    username: str
    university_id: int | None = None
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


# login
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    is_superuser: bool