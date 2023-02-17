from app.api.base.interface import BaseInterface
from app.models.models import Book
from app.models import dto


class GeneralInterface:
    def choose_book(self, user_id: int, book_id: int) -> None:
        pass

    def create_user(self, userDto: dto.User) -> None:
        pass