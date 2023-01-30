from database.sql_commands import DatabaseCommands
from database.client import PgClient
from datetime import date

class Database(DatabaseCommands):
    def __init__(self, database_client: PgClient) -> None:
        self.database_client = database_client

    def setup(self):
        self.database_client.create_conn()
    
    def shutdown(self):
        self.database_client.close_conn()
    
    def get_user(self, user_id: str):
        user = self.database_client.execute_select_command(self.GET_USER, (user_id, ))
        return user[0] if user else user
    
    def create_user(self, user_id: str, username: str, chat_id: str, state: bool, last_visit: date):
        self.database_client.execute_command(self.CREATE_USER, (user_id, username, chat_id, state, last_visit))

    def create_table(self, table_name):
        self.database_client.execute_command(self.CREATE_TABLE_DICT[table_name])

    def get_book(self, book_name, author_name):
        book = self.database_client.execute_select_command(self.GET_BOOK_FROM_BOOKS, (book_name, author_name))
        return book[0] if book else book

    def get_book_from_alist(self, book_id):
        book = self.database_client.execute_select_command(self.GET_BOOK_FROM_ACTIVE_LIST, (book_id, ))
        return book[0] if book else book

    def create_book(self, book_name, author_name):
        self.database_client.execute_command(self.CREATE_BOOK, (book_name, author_name))

    def add_book_to_alist(self, started_reading, user_id, book_id):
        self.database_client.execute_command(self.ADD_BOOK_TO_ACTIVE_LIST, (started_reading, user_id, book_id))
