from db_conn import connection_pool
from psycopg2.extras import RealDictCursor
from psycopg2 import ProgrammingError
from ..config import *
from ..utils.helpers import safe_execute


class DBConnection:

    def __init__(self):
        """Creates a new connection to the database"""
        self.rows_affected: int = 0
        self.last_id: int = 0
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

    def execute(
        self,
        sql: str,
        params: dict = None,
        commit: bool = True,
        key_name: str = None,
    ):
        """Executes a query that makes an update"""
        response = None
        try:
            try:
                with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(sql, params)
                    self.rows_affected += cursor.rowcount
                    response = cursor.fetchone()
                    self.last_id = response[key_name] if response and key_name else None
                    if commit:
                        self.conn.commit()
            except ProgrammingError as e:
                if str(e) == "no results to fetch":
                    if commit:
                        self.conn.commit()
                else:
                    raise e
        except Exception as e:
            self.conn.rollback()
            JSONError.throw_json_error(str(e), 500)
        return response

    def __del__(self):
        connection_pool.putconn(self.conn)
