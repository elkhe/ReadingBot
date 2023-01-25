from database.client import PgClient
from database.sql_commands import DatabaseCommands
from database.db_config import host, db_name, password, user

from datetime import date


database = PgClient()
commands = DatabaseCommands()

#user_id, username, chat_id, state, last_visit
user = (3, 'abobio', 211, True, date.today())

try:
    pass
except Exception as _ex:
    print("Error: ", _ex)
finally:
    print("connection closed")    
