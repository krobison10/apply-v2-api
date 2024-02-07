from ..config import *


class Application:
    db_conn: DBConnection = None

    fields_populated: bool = False  # whether data has been loaded in from db

    aid: int = None
    uid: int = None

    status: int = None
    resume: str = None
    cover_letter: str = None

    title: str = None
    description: str = None
    date: datetime = None
    field: str = None
    position: str = None
    wage: float = None
    job_start: datetime = None

    company: str = None
    industry: str = None
    website: str = None
    phone: str = None

    created_at: datetime = None
    updated_at: datetime = None

    editable: list = [
        "status",
        "resume",
        "cover_letter",
        "title",
        "description",
        "date",
        "field",
        "position",
        "wage",
        "job_start",
        "company",
        "industry",
        "website",
        "phone",
    ]

    def __init__(self, uid=None, aid=None):
        """
        Constructs all the necessary attributes for the application object.

        Parameters:
            aid (int, optional): Auto-incrementing primary key of the application. Defaults to None.
        """

        self.db_conn = DBConnection()
        if aid and uid:
            self.aid = aid
            self.uid = uid
            self.load()

    def load(self):
        """Loads application data from the database based on UID and AID and marks the object as populated."""

        self.set(self.get())
        self.fields_populated = True

    def get(self):
        """
        Retrieves a single application record from the database.

        Returns:
            dict: Application data.
        """

        Validate.required_fields(self, ["aid", "uid"])

        sql = f"""
            SELECT *
            FROM applications a 
            WHERE a.uid = %(uid)s 
                AND a.aid = %(aid)s
            LIMIT 1
        """

        params = {"uid": self.uid, "aid": self.aid}

        return self.db_conn.fetch(sql, params)

    def set(self, data: dict):
        """
        Sets application attributes based on the provided data.

        Parameters:
            data (dict): A dictionary of application data.
        """

        for field in data:
            setattr(self, field, data[field])

    def get_all(self):
        """
        Retrieves all application records for a user from the database.

        Returns:
            list[dict]: List of application data dictionaries.
        """

        Validate.required_fields(self, ["uid"])

        sql = f"""
            SELECT *
            FROM applications a 
            WHERE a.uid = %(uid)s
        """

        params = {"uid": self.uid}

        return self.db_conn.fetchAll(sql, params)

    def save(self, keep_updated_at: bool = False):
        """
        Saves or updates the application record in the database.

        Parameters:
            keep_updated_at (bool, optional): Flag to keep the `updated_at` timestamp unchanged. Defaults to False.

        Returns:
            int: The auto-incrementing primary key (`aid`) of the saved or updated application.
        """

        if self.aid:
            Validate.required_fields(self, ["aid", "uid"])

            updated_at = ""
            if not keep_updated_at:
                updated_at = ", updated_at = NOW()"

            sql = f"""
                UPDATE applications
                SET 
                    uid = %(uid)s, 
                    status = %(status)s, 
                    resume = %(resume)s, 
                    cover_letter = %(cover_letter)s, 
                    title = %(title)s, 
                    description = %(description)s, 
                    date = %(date)s, 
                    field = %(field)s, 
                    position = %(position)s, 
                    wage = %(wage)s, 
                    job_start = %(job_start)s, 
                    company = %(company)s, 
                    industry = %(industry)s, 
                    website = %(website)s, 
                    phone = %(phone)s
                    {updated_at}
                WHERE aid = %(aid)s AND uid = %(uid)s
                RETURNING aid
            """
        else:
            Validate.required_fields(self, ["uid", "status", "title", "company"])
            sql = f"""
                INSERT INTO applications 
                    (uid, status, resume, cover_letter, title, description, date, field, 
                        position, wage, job_start, company, industry, website, phone)
                VALUES 
                    (%(uid)s, %(status)s, %(resume)s, %(cover_letter)s, %(title)s,
                        %(description)s, %(date)s, %(field)s, %(position)s, %(wage)s,
                        %(job_start)s, %(company)s, %(industry)s, %(website)s, %(phone)s)
                RETURNING aid
            """

        params = {
            "aid": self.aid,
            "uid": self.uid,
            "status": self.status,
            "resume": self.resume,
            "cover_letter": self.cover_letter,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "field": self.field,
            "position": self.position,
            "wage": self.wage,
            "job_start": self.job_start,
            "company": self.company,
            "industry": self.industry,
            "website": self.website,
            "phone": self.phone,
        }

        self.db_conn.execute(sql, params)

    def delete(self):
        """
        Deletes the application record from the database.

        Returns:
            bool: True if the delete operation was successful, False otherwise.
        """

        Validate.required_fields(self, ["aid", "uid"])

        sql = f"""
            DELETE FROM applications
            WHERE aid = %(aid)s 
                AND uid = %(uid)s
        """

        params = {"aid": self.aid, "uid": self.uid}

        self.db_conn.execute(sql, params)
