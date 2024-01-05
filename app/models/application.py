from ..config import *


class Application:
    db_conn: DBConnection = None

    aid: int = None
    uid: int = None
    pid: int = None

    status: int = None
    created_at: datetime = None
    updated_at: datetime = None
    resume_url: str = None
    cover_letter_url: str = None

    title: str = None
    description: str = None
    date: datetime = None
    field: str = None
    position: str = None
    wage: float = None
    job_start: datetime = None

    company_name: str = None
    industry: str = None
    website: str = None
    phone: str = None

    def __init__(self, aid=None):
        self.db_conn = DBConnection()

    def get(self, aid=None):
        sql = f"""
        SELECT *
        FROM applications a 
        WHERE a.uid = %(uid)s 
            AND a.aid = %(aid)s
        LIMIT 1
        """

        params = {"uid": self.uid, "aid": aid}

        return self.db_conn.fetch(sql, params)

    def get_all(self):
        sql = f"""
        SELECT *
        FROM applications a 
        WHERE a.uid = %(uid)s
        """

        params = {"uid": self.uid}

        return self.db_conn.fetchAll(sql, params)

    def update_edit_timestamp(self):
        pass

    def update(self, keep_updated_at=False):
        pass

    def save(self):
        pass

    def delete(self):
        pass
