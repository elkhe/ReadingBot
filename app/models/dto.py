from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class User:
    user_id: int
    username: str

@dataclass
class Book:
    bookname: str
    author: str


@dataclass
class Note:
    title: str
    text: str
    date: datetime
    user_id: int
    book_id: int | None


@dataclass
class ActiveList:
    books: List[Book] | None 


@dataclass
class Review:
    title: str
    text: str
    score: int
    user_id: int



