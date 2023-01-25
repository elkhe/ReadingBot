from database.sql_commands import DatabaseCommands
from database.client import PgClient
from datetime import date

class Database(DatabaseCommands):
    def __init__(self, database_client: PgClient) -> None:
        self.database_client = database_client

    def setup(self, setup):
        self.database_client.create_conn()

    def shutdown(self):
        self.database_client.close_conn()
    
    def get_user(self, user_id: str):
        user = self.database_client.execute_select_command(self.GET_USER, user_id)
        return user[0] if user else user
    
    def create_user(self, user_id: str, username: str, chat_id: str, state: bool, last_visit: date):
        self.database_client.execute_command(self.CREATE_USER, (user_id, username, chat_id, state, last_visit))