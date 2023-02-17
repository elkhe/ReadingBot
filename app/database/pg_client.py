import os
from typing import List, Dict

import psycopg2
from dotenv import load_dotenv

from app.config import HOST, DB_NAME, PASSWORD, USER


load_dotenv()


class PgClient:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host=HOST,
            database=DB_NAME,
            password=PASSWORD,
            user=USER
        )        
        self.cursor = self.conn.cursor()

    def execute_command(self, command: str, params: tuple = None):
        with self.conn:
            self.cursor.execute(command, params)

    def execute_select_command(self, command: str, params: tuple = None):
        with self.conn:
            self.cursor.execute(command, params)
            return self.cursor.fetchall()
    
    def close_conn(self):
        self.conn.close()
