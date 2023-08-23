from .db import DBConnection

class User:
    conn = DBConnection()

    def get_user_by_id(self, uid):
        return { 'uid': uid, 'name': 'Kevin'}

    
    def get_all_users(self):
        sql = "SELECT * FROM users"
        return self.conn.fetchAll(sql=sql)
