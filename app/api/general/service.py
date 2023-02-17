from app.models import dto
from app.models.models import Book
from app.api.general.interface import GeneralInterface
from app.api.base.service import BaseService
from datetime import datetime

class GeneralService(BaseService):
    def __init__(self, general_dao: GeneralInterface) -> None:
        super().__init__(general_dao)
        self.general_dao_impl = self.dao

    def start(self, userDto: dto.User) -> None:
        user = self.get_user(userDto)
        if not user:
            self.general_dao_impl.create_user(userDto)

    def choose_book(self, userDto: dto.User, bookDto: dto.Book) -> None:
        book = self.general_dao_impl.get_book(bookDto)
        self.general_dao_impl.choose_book(userDto.user_id, book.book_id)






