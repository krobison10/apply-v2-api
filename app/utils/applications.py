from ..config import *
from ..models.application import Application


class Applications:
    valid_sorts = [
        "relevance",
        "application_date",
        "company_name",
        "position_title",
        "position_wage",
        "priority",
        "created_at",
        "updated_at",
    ]

    default_sort = "created_at"
    default_order = "DESC"
    default_limit = 10
    default_offset = 0

    dates = ["application_date", "job_start", "created_at", "updated_at"]

    match_columns = [
        "position_title",
        "company_name",
        "notes",
        "position_level",
        "company_industry",
        "job_location",
    ]

    def __init__(self, uid=None, aid=None):
        self.db_conn: DBConnection = DBConnection()

        self.uid: int = uid
        self.search_term: str = None

        self.status_filters: list[str] = None
        self.priority_filters: list[int] = None

        # longest amount of days ago to get applications from
        self.from_days_ago: int = None
        # shortest amount of days ago to get applications from
        self.to_days_ago: int = None

        self.sort: str = Applications.default_sort
        self.order: str = Applications.default_order

        self.show_archived: bool = False

        self.limit: int = Applications.default_limit
        self.offset: int = Applications.default_offset

    def set_search_term(self, search_term: str):
        self.search_term = search_term

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
    def get_search_term_filter(search_term: str):
        if not search_term:
            return ""

        individual_terms = search_term.split(" ")
        all_matches = ""
        for i in range(len(individual_terms)):
            term = individual_terms[i]
            term_match = list(
                map(lambda x: f"a.{x} ILIKE '%%{term}%%'", Applications.match_columns)
            )
            term_match = " OR ".join(term_match)

            all_matches += term_match
            if i < len(individual_terms) - 1:
                all_matches += " OR "

        all_matches = f"AND ({all_matches}) \n"

        return all_matches

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

    @staticmethod
    def get_rank_select() -> str:
        # https://www.postgresql.org/docs/current/textsearch-controls.html
        a_rank_text = " || ' ' ||  ".join(
            list(map(lambda x: f"a.{x}", ["company_name", "position_title"]))
        )
        b_rank_text = " || ' ' ||  ".join(
            list(map(lambda x: f"coalesce(a.{x}, '')", ["notes"]))
        )
        c_rank_text = " || ' ' ||  ".join(
            list(
                map(
                    lambda x: f"coalesce(a.{x}, '')",
                    ["job_location", "company_industry", "position_level"],
                )
            )
        )
        normalization = 2  # divides rank by document length
        return f"""
            ts_rank_cd(
                (
                    setweight(to_tsvector({a_rank_text}), 'A') ||
                    setweight(to_tsvector({b_rank_text}), 'B' ) ||
                    setweight(to_tsvector({c_rank_text}), 'C')
                ), query, {normalization})
        """

    @staticmethod
    def get_search_query(search_term) -> tuple[str, str]:
        if not search_term:
            return "", ""
        term_split = " | ".join(map(lambda s: f"{s}:*", search_term.split(" ")))
        return ", to_tsquery(%(term_split)s) query", term_split

    def get(self, count=False):
        """
        Retrieves application records for a user from the database.

        Returns:
            list[dict]: List of application data dictionaries.
        """
        # Validation
        Validate.required_fields(self, ["uid"])

        if self.sort == "relevance" and self.search_term is None:
            JSONError.status_code = 500
            JSONError.throw_json_error("Relevance sort requires a search term")

        # Select columns or count
        base_select = "a.*"

        search_query_select, term_split = Applications.get_search_query(
            self.search_term
        )

        if self.sort == "relevance":
            base_select += f", {Applications.get_rank_select()} AS rank"

        select = base_select if not count else "COUNT(a.*) AS count"

        # Standard filters
        search_term_filter = Applications.get_search_term_filter(self.search_term)

        status_filter = Applications.get_status_filter(self.status_filters)
        priority_filter = Applications.get_priority_filter(self.priority_filters)
        date_filter = Applications.get_date_filters(
            self.from_days_ago, self.to_days_ago, self.sort
        )
        archived_filter = "AND a.archived = 0" if not self.show_archived else ""

        order_clause = ""
        if self.sort == "relevance":
            order_clause = "ORDER BY rank DESC, a.aid DESC"
        else:
            order_clause = (
                f"ORDER BY a.pinned DESC, a.{self.sort} {self.order}, a.aid DESC"
            )

        sort = order_clause if not count else ""

        pagination = f"LIMIT %(limit)s OFFSET %(offset)s" if not count else ""

        sql = f"""
            SELECT {select}
            FROM applications a {search_query_select}
            WHERE a.uid = %(uid)s
            {search_term_filter}
            {status_filter}
            {priority_filter}
            {date_filter}
            {archived_filter}
            {sort}
            {pagination}
        """

        params = {
            "uid": self.uid,
            "term_split": term_split,
            "limit": self.limit,
            "offset": self.offset,
        }

        if count:
            return int(self.db_conn.fetch(sql, params)["count"])
        else:
            return self.db_conn.fetchAll(sql, params)
