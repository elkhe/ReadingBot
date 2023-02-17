from app.api.active_list.interface import ActiveListInterface
from app.models import dto
from app.api.base.dao import BaseImpl
from app.models.models import Book, ActiveList
from datetime import datetime


class ActiveListImpl(ActiveListInterface, BaseImpl):
    def __init__(self, database_client) -> None:
        super().__init__(database_client)


    def add_book(self, user: dto.User, book: Book, date: datetime) -> None:
        self.db.execute_command("""
            INSERT INTO active_list(user_id, book_id, started_reading) 
            VALUES (%s, %s, %s);
        """,
            (user.user_id, book.book_id, date)
        )

    def get_book_id(self, book: Book) -> str | int | None:
        result = self.db.execute_select_command("""
            SELECT user_book_id
              FROM users INNER JOIN active_list
                ON users.user_id = active_list.user_id
             WHERE active_list.book_id = %s;
        """,
            (book.book_id, )
        )
        
        return result[0] if result else None

    def get_list(self, user: dto.User) -> ActiveList | None:
        books = self.db.execute_select_command("""
            SELECT books.book_id, book_name, author_name 
            FROM users 
            INNER JOIN active_list
                ON users.user_id = active_list.user_id
            INNER JOIN books
                ON active_list.book_id = books.book_id
            """, 
            (user.user_id, )
        )
        return ActiveList([Book(book[0], book[1], book[2]) for book in books]) if books else None

    def delete_book(self, book_id: int) -> Book | None:
        deleted_book = self.db.execute_command("""
            DELETE FROM active_list 
            WHERE book_id = %s;
        """,
            (book_id, )    
        )
        