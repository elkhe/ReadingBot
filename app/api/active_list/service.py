from app.models import dto
from app.models.models import Book, ActiveList
from app.api.active_list.interface import ActiveListInterface
from app.api.base.service import BaseService
from datetime import datetime


class ActiveListService(BaseService):
    def __init__(self, active_list_dao: ActiveListInterface) -> None:
        super().__init__(active_list_dao)
        self.active_list_impl = self.dao
        

    def add_book(self, userDto: dto.User, bookDto: dto.Book) -> None:
        book = self.get_book(bookDto)
        if not book:
            book = self.create_book(bookDto)            
        if not self.get_book_id(bookDto):
            self.active_list_impl.add_book(userDto, book, datetime.now())
            return bookDto
        return


    def get_book_id(self, bookDto: dto.Book) -> dto.Book | None:
        book = self.get_book(bookDto)
        if not book:
            return
        return self.active_list_impl.get_book_id(book)


    def get_list(self, userDto: dto.User) -> dto.ActiveList:
        result = self.active_list_impl.get_list(userDto)
        return dto.ActiveList(result.active_list)


    def delete_book(self, bookDto: dto.Book):
        book = self.get_book(bookDto)
        self.active_list_impl.delete_book(book.book_id)

    

