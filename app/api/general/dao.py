from app.api.general.interface import GeneralInterface
from app.models import dto
from app.database.pg_client import PgClient
from datetime import datetime
from app.models.models import Book, User
from app.api.base.dao import BaseImpl


class GeneralImpl(GeneralInterface, BaseImpl):
    def __init__(self, database_client) -> None:
        super().__init__(database_client)

    def choose_book(self, user_id: int, book_id: int) -> None:
        self.db.execute_command("""
            UPDATE users 
            SET book_id = %s
            WHERE user_id = %s;
        """,
            (book_id, user_id)
        )

    def create_user(self, userDto: dto.User):
        self.db.execute_command("""
            INSERT INTO users(user_id, username, chat_id, book_id, last_visit) 
            VALUES (%s, %s, %s, %s, %s); 
        """,
            (
                userDto.user_id, 
                userDto.username,
                userDto.user_id,
                None,
                datetime.now()
            )
        )

        