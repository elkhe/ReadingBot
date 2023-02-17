from pydantic import BaseModel

from typing import List
from datetime import datetime


class Book:
    def __init__(self, book_id: str, bookname: str, author: str) -> None:
        self.book_id = book_id
        self.bookname = bookname
        self.author = author


class ActiveList:
    def __init__(self, book_list: List[Book]) -> None:
        self.active_list = book_list


class User:
    def __init__(self, user_id, username, chat_id, last_visit, active_book=None) -> None:
        self.user_id = user_id
        self.user_name = username
        self.active_book = active_book
        self.chat_id = chat_id
        self.last_visit = last_visit


class Note:
    def __init__(
            self, id: int, title: str, text: str, number: int, date: datetime.now, user_id: int, book_id: int
    ) -> None:
        self.id = id
        self.title = title
        self.text = text
        self.number = number
        self.date = date
        self.user_id = user_id 
        self.book_id = book_id
    




class Review:
    pass