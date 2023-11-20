from ..config import *


class Access:
    @staticmethod
    def check_access():
        if not Access.is_logged_in():
            Access.access_failed()
            JSONError.logged_out()

    @staticmethod
    def check_API_access(bypass_csrf=False):
        if not Access.is_logged_in():
            Access.access_failed()
            JSONError.logged_out()

        r = request.method
        if not bypass_csrf and (
            r == "POST" or r == "PUT" or r == "PATCH" or r == "DELETE"
        ):
            # TODO: CSRF verify
            pass

    @staticmethod
    def access_failed():
        session.clear()

    @staticmethod
    def is_logged_in():
        return session.get("logged_in") == True

    @staticmethod
    def log_visit():
        pass

    @staticmethod
    def redirect_user():
        pass
