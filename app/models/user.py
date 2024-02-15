from ..config import *


class User:

    def __init__(self, uid: int = None):
        self.conn = DBConnection()

        # User fields
        self.uid: int = None

        self.email: str = None
        self.firstname: str = None
        self.lastname: str = None
        self.phone: str = None
        self.username: str = None
        self.created_at: datetime = None
        self.updated_at: datetime = None

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

    def get_by_email(self, with_credentials=False) -> dict:

        sql = f"""
        SELECT u.* {", c.hashed_pass, c.salt" if with_credentials else ""}
        FROM users u 
        {"JOIN credentials c ON c.uid = u.uid" if with_credentials else ""}
        WHERE u.email = %(email)s
        """

        params = {"email": self.email}

        return self.conn.fetch(sql, params)

    def create(self) -> int:
        sql = """
        INSERT INTO users (email, firstname, lastname, phone, username)
        VALUES (%(email)s, %(firstname)s, %(lastname)s, %(phone)s, %(username)s)
        RETURNING uid
        """

        Validate.required_fields(self, ["email"])

        params = {
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "phone": self.phone,
            "username": self.username,
        }

        self.conn.execute(sql, params)

        if self.conn.rows_affected < 1:
            JSONError.status_code = 500
            JSONError.throw_json_error("User creation failed")

        return self.conn.rows_affected

    def get_all(self) -> dict:
        sql = "SELECT * FROM users"
        return self.conn.fetchAll(sql)
