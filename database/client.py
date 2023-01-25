import psycopg2

class PgClient:
    def __init__(self) -> None:
        self.conn = None
    
    def create_conn(self, host, db_name, password, user):
        self.conn = psycopg2.connect(
            host=host,
            database=db_name,
            password=password,
            user=user
        )
    
    def close_conn(self):
        self.conn.close()

    def execute_command(self, command: str, params: tuple):
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(command, params)

    def execute_select_command(self, command: str, params: tuple):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(command, params)
            return cursor.fetchall()
