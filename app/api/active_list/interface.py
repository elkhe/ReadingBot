from app.models import dto
from datetime import datetime


class ActiveListInterface:   
    def add_book(self, user: dto.User, book: dto.Book, date: datetime):
        pass

    def get_book_id(self, book_id: int):
        pass

    def get_list(self, user: dto.User):
        pass

    def delete_book(self, book_id: int):
        pass
