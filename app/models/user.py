from ..config import *


class User:
    conn = None

    # User fields
    uid: int

    email: str
    firstname: str
    lastname: str
    phone: str
    username: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, uid: int = None):
        self.conn = DBConnection()

        if uid:
            self.uid = uid
            data = self.get_by_id()

            if not data:
                JSONError.status_code = 404
                JSONError.throw_json_error("User not found")

            self.email = data["email"]
            self.firstname = data["firstname"]
            self.lastname = data["lastname"]
            self.phone = data["phone"]
            self.username = data["username"]
            self.created_at = data["created_at"]
            self.updated_at = data["updated_at"]

    def get_by_id(self) -> dict:
        sql = """
        SELECT *
        FROM users u 
        WHERE u.uid = %(uid)s
        """

        params = {"uid": self.uid}

        return self.conn.fetch(sql, params)

    def get_all(self) -> dict:
        sql = "SELECT * FROM users"
        return self.conn.fetchAll(sql)
