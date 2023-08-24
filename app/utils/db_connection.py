from db_conn import connection_pool
from psycopg2.extras import RealDictCursor

class DBConnection:
    
    def __init__(self):
        """Creates a new connection to the database""" 
        self.conn = connection_pool.getconn()
        self._init_connection()
        
        
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
    
    
    def _init_connection(self):
        pass
        
    
    def __del__(self):
        connection_pool.putconn(self.conn)
