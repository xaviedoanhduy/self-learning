from pydantic import BaseModel, ValidationError, validator
from pydantic.dataclasses import dataclass


@dataclass
class Book:
    title: str
    pages: int

    @validator("pages")
    def pages_must_be_positive(cls, v: int):
        if v < 0:
            raise ValueError("Pages must be a positive integer")
        return v


class Author(BaseModel):
    name: str
    age: int

    @validator("age")
    def age_must_be_positive(cls, v: int):
        if v < 0:
            raise ValueError("Age must be a positive integer")
        return v


def main() -> None:
    # Valid input
    book = Book(title="1984", pages=328)  # pages will be converted to int


    # Invalid input – will raise a ValidationError
    try:
        bad_book = Book(title="The Hobbit", pages="three hundred")
    except ValidationError as e:
        print(e)

    author = Author(name="J.K. Rowling", age=60)
    print(author.model_dump())


if __name__ == "__main__":
    main()
