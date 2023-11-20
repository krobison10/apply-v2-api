from ..config import *


class Interview:
    conn: DBConnection = None

    uid: int = None

    iid: int = None
    aid: int = None

    date: datetime = None
    modality: int = None
    location: str = None
    created_at: datetime = None
    updated_at: datetime = None

    application: Application = None

    def __init__(self, iid=None):
        self.conn = DBConnection()

    def get(self, iid: int, expand: bool = False):
        extra_select = ""
        if expand:
            extra_select = """
            LEFT JOIN postings p
                ON a.pid = p.pid
            LEFT JOIN companies c
                ON c.cid = p.cid
            """

        sql = f"""
        SELECT i.* {", a.*, p.*, c.* " if expand else ""}
        FROM interviews i 
        LEFT JOIN applications a
            ON i.aid = a.aid
        {extra_select}
        WHERE a.uid = %(uid)s 
            AND i.iid = %(iid)s
        LIMIT 1
        """

        params = {"uid": self.uid, "iid": iid}

        return self.conn.fetch(sql, params)

    def get_all(self, expand: bool = False):
        extra_select = ""
        if expand:
            extra_select = """
            LEFT JOIN postings p
                ON a.pid = p.pid
            LEFT JOIN companies c
                ON c.cid = p.cid
            """

        sql = f"""
        SELECT i.* {", a.*, p.*, c.* " if expand else ""}
        FROM interviews i 
        LEFT JOIN applications a
            ON i.aid = a.aid
        {extra_select}
        WHERE a.uid = %(uid)s
        """

        params = {"uid": self.uid}

        return self.conn.fetchAll(sql, params)

    def update_edit_timestamp(self):
        pass

    def update(self, keep_updated_at=False):
        pass

    def save(self):
        pass

    def delete(self):
        pass
