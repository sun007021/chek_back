from fastapi import FastAPI

from domain.user import user_router
from domain.book import book_router

app = FastAPI()

app.include_router(user_router.router)
app.include_router(book_router.router)