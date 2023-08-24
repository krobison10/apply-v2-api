from db_conn import connection
from psycopg2.extras import RealDictCursor

class DBConnection:
    conn = None
    
    def __init__(self):
        """Creates a new connection to the database""" 
        self.conn = connection
        self._init_connection()        
        
        
    def fetch(self, sql, params = None):
        """Fetches one result"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            return cursor.fetch()
        

    def fetchAll(self, sql, params = None):
        """Fetches all results"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    
    def _init_connection(self):
        """Initializes the connection to the db"""
        cur = self.conn.cursor()
        cur.execute("SET search_path TO apply")
        self.conn.commit()
    
    
    def _close(self):
        """Closes the connection to the database"""
        self.conn.close()
        
    
    def __del__(self):
        """Destructor that calls _close()"""
        self._close()
