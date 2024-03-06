from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    image = Column(String, nullable=True)
    university_id = Column(Integer, ForeignKey("university.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    university = relationship("University", backref="users")

class University(Base):
    __tablename__ = "university"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    address = Column(String, nullable=True)

# 책 모델
class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title= Column(String, nullable=False)
    author= Column(String, nullable=False)
    isbn= Column(String, nullable=False)
    publisher= Column(String, nullable=False)
    publicationdate= Column(String, nullable=False)
    image= Column(String, nullable=True)

# 거래 글 모델
class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    subject= Column(String, nullable=False)
    content= Column(String, nullable=False)
    book_id= Column(Integer, ForeignKey("book.id"))
    title= Column(String, nullable=False)
    author= Column(String, nullable=False)
    isbn= Column(String, nullable=False)
    publisher= Column(String, nullable=False)
    publicationdate= Column(String, nullable=False)
    image= Column(String, nullable=True)
    create_date = Column(DateTime, nullable=False)
