from ..config import *
import hashlib
from os import urandom


class Credentials:
    def __init__(self, email: str, supplied_password: str):
        self.email = email
        self.supplied_password = supplied_password
        self.conn = DBConnection()

    def get_credentials(self) -> dict:
        sql = """
        SELECT c.hashed_pass, c.salt
        FROM credentials c
        JOIN users u 
            ON c.uid = u.uid
        WHERE u.email = %(email)s
        """

        params = {"email": self.email}

        return self.conn.fetch(sql, params)

    def verify_user(self):
        credentials = self.get_credentials()
        if not credentials:  # TODO: find a better solution for this
            # Credentials not found, create some
            self.create()
            return
        hashed_pass = credentials["hashed_pass"]
        salt = credentials["salt"]
        if not Credentials.verify_password(hashed_pass, self.supplied_password, salt):
            JSONError.status_code = 401
            JSONError.throw_json_error("Invalid email or password")

    def create(self) -> int:
        hashed_pass, salt = Credentials.create_hash(self.supplied_password)

        sql = """
        INSERT INTO credentials (uid, hashed_pass, salt)
        VALUES ((SELECT u.uid FROM users u WHERE u.email = %(email)s), %(hashed_pass)s, %(salt)s)
        """

        params = {
            "email": self.email,
            "hashed_pass": hashed_pass,
            "salt": salt,
        }

        self.conn.execute(sql, params)
        return self.conn.rows_affected

    @staticmethod
    def verify_password(hashed_password: str, password: str, salt: str) -> bool:
        salt_bytes: bytes = bytes.fromhex(salt)
        return hashed_password == Credentials.hash_password(password, salt_bytes)

    @staticmethod
    def create_hash(password: str) -> tuple[str, str]:
        salt: bytes = urandom(64)
        hashed_pass: str = Credentials.hash_password(password, salt)
        return hashed_pass, salt.hex()

    @staticmethod
    def hash_password(password: str, salt: bytes) -> str:
        salted_password: bytes = password.encode() + salt
        hashed_password: str = Credentials.hash_value(salted_password)
        return hashed_password

    @staticmethod
    def hash_value(value: bytes) -> str:
        return hashlib.sha256(value).hexdigest()
