from ..config import *


class Interview:
    required_fields = ["aid", "date", "modality"]

    def __init__(self, uid=None, iid=None):
        self.uid: int = uid
        self.fields_populated: bool = False

        self.iid: int = iid
        self.aid: int = None

        self.date: datetime = None
        self.modality: str = None
        self.location: str = None
        self.notes: str = None
        self.type: str = None

        self.created_at: datetime = None
        self.updated_at: datetime = None

        self.conn = DBConnection()

        if uid and iid:
            self.load()

    def get(self):

        Validate.required_fields(self, ["uid", "iid"])

        sql = f"""
        SELECT i.*, a.status, a.position_title, a.company_name, a.notes AS application_notes
        FROM interviews i 
        RIGHT JOIN applications a
            ON i.aid = a.aid
        WHERE a.uid = %(uid)s 
            AND i.iid = %(iid)s
        LIMIT 1
        """

        params = {"uid": self.uid, "iid": self.iid}

        return self.conn.fetch(sql, params)

    def load(self):
        """Loads interview data from the database based on UID and AID and marks the object as populated."""
        self.set(self.get())
        self.fields_populated = True

    def set(self, data: dict):
        """
        Sets interview attributes based on the provided data.

        Parameters:
            data (dict): A dictionary of interview data.
        """

        for field in data:
            if hasattr(self, field):
                setattr(self, field, data[field])

    def save(self, keep_updated_at: bool = False):
        """
        Saves or updates the interview record in the database.

        Parameters:
            keep_updated_at (bool, optional): Flag to keep the `updated_at` timestamp unchanged. Defaults to False.

        Returns:
            int: The auto-incrementing primary key (`iid`) of the saved or updated interview.
        """

        Validate.required_fields(self, ["uid", "date", "modality"])

        if self.iid:
            updated_at = ""
            if not keep_updated_at:
                updated_at = ", updated_at = NOW()"

            sql = f"""
                UPDATE interviews i
                SET 
                    aid = %(aid)s,
                    date = %(date)s,
                    modality = %(modality)s,
                    location = %(location)s,
                    notes = %(notes)s,
                    type = %(type)s
                    {updated_at}
                FROM applications a
                WHERE 
                    i.iid = %(iid)s 
                    AND a.uid = %(uid)s
                    AND a.aid = i.aid
                RETURNING i.iid
            """
        else:
            sql = f"""
                INSERT INTO interviews 
                    (aid, date, modality, location, notes, type)
                VALUES 
                    (%(aid)s, %(date)s, %(modality)s, %(location)s, %(notes)s, %(type)s)
                RETURNING iid
            """

        params = {
            "iid": self.iid,
            "uid": self.uid,
            "aid": self.aid,
            "date": self.date,
            "modality": self.modality,
            "location": self.location,
            "notes": self.notes,
            "type": self.type,
        }

        response = self.conn.execute(sql, params)
        return response["iid"]

    def delete(self) -> int:
        """
        Deletes the interview record from the database.

        Returns:
            bool: True if the delete operation was successful, False otherwise.
        """

        Validate.required_fields(self, ["iid", "uid"])

        sql = f"""
            DELETE FROM interviews i
            USING applications a
            WHERE i.aid = a.aid 
                AND i.iid = %(iid)s 
                AND a.uid = %(uid)s
        """

        params = {"iid": self.iid, "uid": self.uid}

        self.conn.execute(sql, params)
        return self.conn.rows_affected
