from ..utils.db_connection import DBConnection

class User:
    conn = None
    
    # User fields
    uid: int = None
    
    def __init__(self, uid: int = None):
        self.conn = DBConnection()
        
        if uid:
            self.uid = uid
    

    def get_user_by_id(self) -> dict:
        sql = """
        SELECT *
        FROM users u 
        WHERE u.uid = %(uid)s
        """

        params = {
            "uid": self.uid
        }
        
        return self.conn.fetch(sql, params)
    
    
    def get_all_users(self) -> dict:
        sql = "SELECT * FROM users"
        return self.conn.fetchAll(sql=sql)
