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
        self.email_verified: int = None

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
            self.email_verified = data["email_verified"]

    def get_by_id(self) -> dict:
        sql = """
        SELECT *
        FROM users u 
        WHERE u.uid = %(uid)s
        """

        params = {"uid": self.uid}

        result = self.conn.fetch(sql, params)
        self.set(result)
        return result

    def get_by_email(self, with_credentials=False) -> dict:

        sql = f"""
        SELECT u.* {", c.hashed_pass, c.salt" if with_credentials else ""}
        FROM users u 
        {"JOIN credentials c ON c.uid = u.uid" if with_credentials else ""}
        WHERE u.email = %(email)s
        """

        params = {"email": self.email}

        result = self.conn.fetch(sql, params)
        if result:
            self.set(result)
        return result

    def set(self, data: dict):
        for field in data:
            if hasattr(self, field):
                setattr(self, field, data[field])

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

        self.conn.execute(sql, params, key_name="uid")

        if self.conn.rows_affected < 1:
            JSONError.status_code = 500
            JSONError.throw_json_error("User creation failed")

        self.uid = self.conn.last_id
        return self.conn.rows_affected

    def create_activation(self, code: int) -> int:
        sql = """
        INSERT INTO activation (uid, code)
        VALUES (%(uid)s, %(code)s)
        ON CONFLICT (uid) DO UPDATE
        SET uid = %(uid)s, code = %(code)s
        """
        params = {"uid": self.uid, "code": code}
        self.conn.execute(sql, params)

        if self.conn.rows_affected < 1:
            JSONError.status_code = 500
            JSONError.throw_json_error("Activation creation failed")

        return self.conn.rows_affected

    def get_activation(self) -> dict:
        sql = """
        SELECT *
        FROM activation
        WHERE uid = %(uid)s
        """

        params = {"uid": self.uid}

        return self.conn.fetch(sql, params)

    def delete_activation(self) -> int:
        sql = """
        DELETE FROM activation
        WHERE uid = %(uid)s
        """

        params = {"uid": self.uid}

        self.conn.execute(sql, params)

        if self.conn.rows_affected < 1:
            JSONError.status_code = 500
            JSONError.throw_json_error("Activation deletion failed")

        return self.conn.rows_affected

    def save(self) -> int:
        sql = """
        UPDATE users
        SET
        firstname = %(firstname)s, 
        lastname = %(lastname)s, 
        phone = %(phone)s, 
        username = %(username)s,
        email_verified = %(email_verified)s
        WHERE uid = %(uid)s
        """

        Validate.required_fields(self, ["uid"])

        params = {
            "uid": self.uid,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "phone": self.phone,
            "username": self.username,
            "email_verified": self.email_verified,
        }

        self.conn.execute(sql, params)

        if self.conn.rows_affected < 1:
            JSONError.status_code = 500
            JSONError.throw_json_error("User update failed")

        return self.conn.rows_affected

    def delete(self) -> int:
        sql = """
        DELETE FROM users
        WHERE uid = %(uid)s
        """

        Validate.required_fields(self, ["uid"])

        params = {"uid": self.uid}

        self.conn.execute(sql, params)

        if self.conn.rows_affected < 1:
            JSONError.status_code = 500
            JSONError.throw_json_error("User deletion failed")

        return self.conn.rows_affected

    def get_all(self) -> dict:
        sql = "SELECT * FROM users"
        return self.conn.fetchAll(sql)
