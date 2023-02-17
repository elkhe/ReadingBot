from app.models.models import Book, User
from app.models import dto


class BaseService:
    def __init__(self, dao) -> None:
        self.dao = dao 

    def get_book(self, bookDto: dto.Book) -> Book:
        return self.dao.get_book(bookDto)

    def create_book(self, bookDto: dto.Book) -> Book:
        return self.dao.create_book(bookDto)

    def get_user(self, userDto: dto.User) -> User | None:
        user: User = self.dao.get_user(userDto)
        return user if user else None

    def get_active_book(self, userDto: dto.User) -> dto.Book | None:
        book: Book = self.dao.get_active_book(userDto.user_id)
        if book: 
            return dto.Book(
                bookname=book.bookname,
                author=book.author
            )
        else: 
            return None
            

