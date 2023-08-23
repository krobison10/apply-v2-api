from db_conn import connection

class DBConnection:
    conn = None
    
    def __init__(self):
        self.conn = connection
        cur = self.conn.cursor()
        cur.execute("SET search_path TO apply")
        self.conn.commit()
        
        
    def fetch(self, sql, params = None):
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetch()
        

    def fetchAll(self, sql, params = None):
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    
    def close(self):
        self.conn.close()
        
    
    def __del__(self):
        self.close()