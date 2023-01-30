import psycopg2

class PgClient:
    def __init__(self, host, db_name, password, user) -> None:
        self.conn = None
        self.host = host
        self.db_name = db_name  
        self.password = password
        self.user = user
    
    def create_conn(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.db_name,
            password=self.password,
            user=self.user
        )
    
    def close_conn(self):
        self.conn.close()

    def execute_command(self, command: str, params: tuple = None):
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(command, params)

    def execute_select_command(self, command: str, params: tuple = None):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(command, params)
            return cursor.fetchall()
