from db_conn import connection_pool
from psycopg2.extras import RealDictCursor
from ..config import *
from ..utils.helpers import safe_execute


class DBConnection:
    rows_affected: int = 0
    last_id: int = 0

    def __init__(self):
        """Creates a new connection to the database"""
        self.conn = connection_pool.getconn()

    def fetch(self, sql: str, params: dict = None):
        """Fetches one result"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def fetchAll(self, sql: str, params: dict = None):
        """Fetches all results"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def execute(self, sql: str, params: dict = None, commit: bool = True):
        """Executes a query that makes an update"""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(sql, params)
                self.rows_affected += cursor.rowcount
                response = safe_execute(
                    cursor.fetchone, None
                )  # fetchone() isn't really working
                self.last_id = response[0] if response else None
                if commit:
                    self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            JSONError.throw_json_error(str(e), 500)

    def __del__(self):
        connection_pool.putconn(self.conn)
