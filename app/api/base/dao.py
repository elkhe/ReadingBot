from app.models.models import Book, User
from app.api.base.interface import BaseInterface
from app.models import dto
from app.database.pg_client import PgClient


class BaseImpl:
    def __init__(self, database_client: PgClient) -> None:
        self.db = database_client


    def get_book(self, bookDto: dto.Book) -> Book | None:
        book = self.db.execute_select_command("""
            SELECT book_id, book_name, author_name
            FROM books
            WHERE book_name = %s AND author_name = %s; 
            """,
            (bookDto.bookname, bookDto.author)
        )
        return Book(*book[0]) if book else None
        

    def create_book(self, bookDto: dto.Book) -> Book:
        self.db.execute_command("""
            INSERT INTO books(book_name, author_name) 
            VALUES (%s, %s); 
            """,
            (bookDto.bookname, bookDto.author)    
        )
        book = self.get_book(bookDto)
        return book


    def get_user(self, userDto: dto.User) -> User | None:
        user_raw = self.db.execute_select_command("""
            SELECT *
              FROM users
             WHERE users.user_id = %s 
        """,
            (userDto.user_id, )
        )
        print(user_raw == True)
        return User(*user_raw[0]) if user_raw else None

    def get_active_book(self, user_id) -> Book | None:
        active_book = self.db.execute_select_command("""
            SELECT books.book_id, book_name, author_name
            FROM books 
            WHERE books.book_id = 
                (SELECT book_id 
                FROM users 
                WHERE users.user_id = %s);
        """,
            (user_id, )
        )
        return Book(*active_book[0]) if active_book else None