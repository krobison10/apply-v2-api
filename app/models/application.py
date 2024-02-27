from ..config import *


class Application:
    # Fields that are not user editable
    non_editable: list = ["aid", "uid", "created_at", "updated_at"]

    # Fields that are required for this resources
    required_fields = ["status", "position_title", "company_name"]

    valid_statuses = [
        "not submitted",
        "submitted",
        "responded",
        "rejected",
        "interviewing",
        "offer received",
        "withdrawn",
        "closed",
    ]

    valid_priorities_map = {
        "none": 0,
        "lowest": 1,
        "low": 2,
        "medium": 3,
        "high": 4,
        "highest": 5,
    }

    def __init__(self, uid=None, aid=None):
        """
        Constructs all the necessary attributes for the application object.

        Parameters:
            aid (int, optional): Auto-incrementing primary key of the application. Defaults to None.
        """

        self.db_conn: DBConnection = DBConnection()

        self.fields_populated: bool = False  # whether data has been loaded in from db

        self.aid: int = aid
        self.uid: int = uid

        self.status: int = None
        self.resume_url: str = None
        self.cover_letter_url: str = None
        self.position_title: str = None
        self.notes: str = None
        self.application_date: datetime = None
        self.position_level: str = None
        self.position_wage: int = None
        self.company_name: str = None
        self.company_industry: str = None
        self.company_website: str = None
        self.created_at: datetime = None
        self.updated_at: datetime = None
        self.posting_url: str = None
        self.job_location: str = None
        self.posting_source: str = None
        self.job_start: datetime = None
        self.priority: int = None
        self.pinned: int = 0
        self.archived: int = 0

        if aid and uid:
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
            if hasattr(self, field):
                setattr(self, field, data[field])

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
                    resume_url = %(resume_url)s, 
                    cover_letter_url = %(cover_letter_url)s, 
                    position_title = %(position_title)s, 
                    notes = %(notes)s, 
                    application_date = %(application_date)s, 
                    position_level = %(position_level)s, 
                    position_wage = %(position_wage)s, 
                    company_name = %(company_name)s, 
                    company_industry = %(company_industry)s, 
                    company_website = %(company_website)s, 
                    posting_url = %(posting_url)s, 
                    job_location = %(job_location)s, 
                    posting_source = %(posting_source)s, 
                    job_start = %(job_start)s, 
                    priority = %(priority)s
                    {updated_at}
                WHERE aid = %(aid)s
                RETURNING aid
            """
        else:
            Validate.required_fields(
                self, ["uid", "status", "position_title", "company_name"]
            )

            sql = f"""
                INSERT INTO applications 
                    (uid, status, resume_url, cover_letter_url, position_title, notes, application_date, 
                    position_level, position_wage, company_name, company_industry, company_website, 
                    posting_url, job_location, posting_source, job_start, priority)
                VALUES 
                    (%(uid)s, %(status)s, %(resume_url)s, %(cover_letter_url)s, %(position_title)s, 
                    %(notes)s, %(application_date)s, %(position_level)s, %(position_wage)s, 
                    %(company_name)s, %(company_industry)s, %(company_website)s, %(posting_url)s, 
                    %(job_location)s, %(posting_source)s, %(job_start)s, %(priority)s)
                RETURNING aid
            """

        params = {
            "aid": self.aid,
            "uid": self.uid,
            "status": self.status,
            "resume_url": self.resume_url,
            "cover_letter_url": self.cover_letter_url,
            "position_title": self.position_title,
            "notes": self.notes,
            "application_date": self.application_date,
            "position_level": self.position_level,
            "position_wage": self.position_wage,
            "company_name": self.company_name,
            "company_industry": self.company_industry,
            "company_website": self.company_website,
            "posting_url": self.posting_url,
            "job_location": self.job_location,
            "posting_source": self.posting_source,
            "job_start": self.job_start,
            "priority": self.priority,
        }

        response = self.db_conn.execute(sql, params)
        return response["aid"]

    def pin(self) -> int:
        """
        Pins the application record in the database.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """

        Validate.required_fields(self, ["aid", "uid"])

        sql = f"""
            UPDATE applications
            SET pinned = %(pinned)s
            WHERE aid = %(aid)s 
                AND uid = %(uid)s
        """

        params = {"aid": self.aid, "uid": self.uid, "pinned": self.pinned}

        self.db_conn.execute(sql, params)
        return self.db_conn.rows_affected

    def archive(self) -> int:
        """
        Archives the application record in the database.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """

        Validate.required_fields(self, ["aid", "uid"])

        sql = f"""
            UPDATE applications
            SET archived = %(archived)s
            WHERE aid = %(aid)s 
                AND uid = %(uid)s
        """

        params = {"aid": self.aid, "uid": self.uid, "archived": self.archived}

        self.db_conn.execute(sql, params)
        return self.db_conn.rows_affected

    def delete(self) -> int:
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
        return self.db_conn.rows_affected
