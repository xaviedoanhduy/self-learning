from __future__ import annotations
import secrets
import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)


DB_FILE = Path("books.db")
DB_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


# SQLAlchemy ORM model

class Book(Base):
    __tablename__ = "books"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: secrets.token_hex(12))
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    pages: Mapped[int] = mapped_column(Integer, default=0)
    

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    

class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    pages: int
    
    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    title="Book Management API",
    version="3.1.0",
    description="A simple CRUD API for managing books using FastAPI and SQLAlchemy ORM.",
)


# Create DB tables
Base.metadata.create_all(bind=engine)


# CRUD Endpoints
@app.post("/books/", response_model=BookResponse, tags=["Books"], summary="Create a new book")
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    book = Book(**book_data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.get("/books/{book_id}", response_model=BookResponse, tags=["Books"], summary="Get a book by ID")
def get_book(book_id: str, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/books/", response_model=list[BookResponse], tags=["Books"], summary="List all books")
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.put("/books/{book_id}", response_model=BookResponse, tags=["Books"], summary="Update a book by ID")
def update_book(book_id: str, book_data: BookCreate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book_data.model_dump().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", tags=["Books"], summary="Delete a book by ID")
def delete_book(book_id: str, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted successfully"}


@app.get("/ping", summary="Health check endpoint")
def ping():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)