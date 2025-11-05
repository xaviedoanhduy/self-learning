from __future__ import annotations
import json
import secrets
import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, dataclasses
from typing import Dict, List
from pathlib import Path
from contextlib import asynccontextmanager



DB_FILE = Path("books.json")

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_db()
    yield
    save_db()


app = FastAPI(
    title="Book Management API",
    version="2.0.0",
    description="A simple CRUD API for managing books using FastAPI and dataclasses.",
    lifespan=lifespan,
)


def generate_id() -> str:
    return secrets.token_hex(12)


@dataclasses.dataclass
class Book:
    title: str
    author: str
    pages: int = 0
    id: str = dataclasses.Field(default_factory=generate_id)


class BookCreate(BaseModel):
    title: str
    author: str
    pages: int = 0
    
    class Config:
        from_attributes = True


class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    pages: int
    
    class Config:
        from_attributes = True

    @classmethod
    def from_book(cls, book: Book) -> BookResponse:
        return cls(**book.__dict__)


books_db: Dict[str, Book] = {}


def save_db():
    with DB_FILE.open("w", encoding="utf-8") as f:
        json.dump([book.__dict__ for book in books_db.values()], f, indent=4, ensure_ascii=False)


def load_db():
    global books_db
    if DB_FILE.exists():
        with DB_FILE.open(encoding="utf-8") as f:
            books = json.load(f)
            books_db = {b["id"]: Book(**b) for b in books}
    else:
        books_db = {}


@app.get("/ping", summary="Health check endpoint")
def ping() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/books/", response_model=BookResponse, tags=["Books"], summary="Create a new book")
def create_book(book: BookCreate) -> BookResponse:
    new_book: Book = Book(**book.dict())
    books_db[new_book.id] = new_book
    save_db()
    return BookResponse.model_validate(book)


@app.get("/books/{book_id}", response_model=BookResponse, tags=["Books"], summary="Get a book by ID")
def get_book(book_id: str) -> BookResponse:
    book: Book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.model_validate(book)


@app.put("/books/{book_id}", response_model=BookResponse, tags=["Books"], summary="Update a book by ID")
def update_book(book_id: str, updated_book: BookCreate) -> BookResponse:
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    book: Book = books_db[book_id]
    book.title = updated_book.title
    book.author = updated_book.author
    book.pages = updated_book.pages
    save_db()
    return BookResponse.model_validate(book)


@app.delete("/books/{book_id}", tags=["Books"], summary="Delete a book by ID")
def delete_book(book_id: str) -> Dict[str, str]:
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del books_db[book_id]
    save_db()
    return {"detail": "Book deleted successfully"}


@app.get("/books/")
def list_books() -> List[BookResponse]:
    return [BookResponse.model_validate(book) for book in books_db.values()]


if __name__ == "__main__":
    load_db()  # preload data before app starts manually
    uvicorn.run(app, host="0.0.0.0", port=8000)
