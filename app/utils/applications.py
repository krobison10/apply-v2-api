from ..config import *
from ..models.application import Application


class Applications:
    valid_sorts = [
        "application_date",
        "company_name",
        "position_title",
        "position_wage",
        "priority",
        "created_at",
        "updated_at",
    ]

    dates = ["application_date", "job_start", "created_at", "updated_at"]

    def __init__(self, uid=None, aid=None):
        self.db_conn: DBConnection = DBConnection()

        self.uid: int = uid

        # for feed queries
        self.status_filters: list[str] = None
        self.priority_filters: list[int] = None

        # longest amount of days ago to get applications from
        self.from_days_ago: int = None
        # shortest amount of days ago to get applications from
        self.to_days_ago: int = None

        self.sort: str = "created_at"
        self.order: str = "DESC"

        self.limit: int = 10
        self.offset: int = 0

    def set_sort(self, sort: str):
        if sort:
            if sort.lower() not in Applications.valid_sorts:
                JSONError.status_code = 422
                JSONError.throw_json_error(f"Invalid sort: {sort}")
            self.sort = sort.lower()

    def set_order(self, order: str):
        if order:
            if order.lower() not in ["asc", "desc"]:
                JSONError.status_code = 422
                JSONError.throw_json_error(f"Invalid order: {order}")
            self.order = order.upper()

    def set_limit(self, limit: int):
        self.limit = limit

    def set_offset(self, offset: int):
        self.offset = offset

    def set_status_filters(self, status_filters: list[str]):
        for filter in status_filters:

            if (
                filter
                and filter.lower().replace("_", " ") not in Application.valid_statuses
            ):
                JSONError.status_code = 422
                JSONError.throw_json_error(f"Invalid status filter: {filter}")

        self.status_filters = list(
            map(lambda x: str(x).lower().replace("_", " "), status_filters)
        )

    def set_priority_filters(self, priority_filters: list[str]):
        for filter in priority_filters:
            if filter and filter.lower() not in Application.valid_priorities_map.keys():
                JSONError.status_code = 422
                JSONError.throw_json_error(f"Invalid priority filter: {filter}")

        self.priority_filters = list(
            map(
                lambda filter: str(Application.valid_priorities_map[filter.lower()]),
                priority_filters,
            )
        )

    def set_date_filters(self, from_days_ago: int, to_days_ago: int):
        self.from_days_ago = from_days_ago
        self.to_days_ago = to_days_ago

    @staticmethod
    def get_date_filters(from_days_ago: int, to_days_ago: int, col: str = "created_at"):
        filter = ""
        filter_col = col if col in Applications.dates else "created_at"
        if from_days_ago or from_days_ago == 0:
            filter += f"AND a.{filter_col} >= CURRENT_DATE - INTERVAL '{from_days_ago} DAY' \n"
        if to_days_ago:
            filter += (
                f"AND a.{filter_col} <= CURRENT_DATE - INTERVAL '{to_days_ago} DAY' \n"
            )

        return filter

    @staticmethod
    def get_status_filter(status_filters: list[str] = []):
        list = "', '".join(status_filters)
        return f"AND a.status IN ('{list}') \n" if len(status_filters) > 0 else ""

    @staticmethod
    def get_priority_filter(priority_filters: list[int] = []):
        list = ", ".join(priority_filters)
        return f"AND a.priority IN ({list}) \n" if len(priority_filters) > 0 else ""

    def get(self, count=False):
        """
        Retrieves application records for a user from the database.

        Returns:
            list[dict]: List of application data dictionaries.
        """

        select = "a.*" if not count else "COUNT(a.*) AS count"

        status_filter = self.get_status_filter(self.status_filters)
        priority_filter = self.get_priority_filter(self.priority_filters)
        date_filter = self.get_date_filters(
            self.from_days_ago, self.to_days_ago, self.sort
        )

        pagination = f"LIMIT %(limit)s OFFSET %(offset)s" if not count else ""

        sort = f"ORDER BY {self.sort} {self.order}" if not count else ""

        Validate.required_fields(self, ["uid"])

        sql = f"""
            SELECT {select}
            FROM applications a 
            WHERE a.uid = %(uid)s
            {status_filter}
            {priority_filter}
            {date_filter}
            {sort}
            {pagination}
        """

        print(sql)

        params = {"uid": self.uid, "limit": self.limit, "offset": self.offset}

        if count:
            return int(self.db_conn.fetch(sql, params)["count"])
        else:
            return self.db_conn.fetchAll(sql, params)
