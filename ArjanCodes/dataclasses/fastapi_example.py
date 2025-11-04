import secrets
import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Book(BaseModel):
    title: str
    author: str
    pages: int


books_db: dict[str, Book] = {}


def generate_book_id() -> str:
    return secrets.token_hex(12)


@app.post("/books/", response_model=Book)
def create_book(book: Book) -> Book:
    book_id = generate_book_id()
    books_db[book_id] = book
    return book


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: str) -> Book:
    book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: str, updated_book: Book) -> Book:
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db[book_id] = updated_book
    return updated_book


@app.delete("/books/{book_id}")
def delete_book(book_id: str) -> dict[str, str]:
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del books_db[book_id]
    return {"detail": "Book deleted successfully"}


@app.get("/books/")
def list_books():
    return [{"id": book_id, "book": book} for book_id, book in books_db.items()]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
