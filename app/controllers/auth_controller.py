from ..config import *


def login(email: str, password: str) -> dict:
    check_logged_in()

    email = Validate.email(email)

    user = User()
    user.email = email
    user_data = user.get_by_email()

    credentials = Credentials(email, password)

    if not user_data:  # user does not exist
        user.create()
        credentials.create()
    else:
        credentials.verify_user()

    # success
    session["logged_in"] = True
    session["valid_uid"] = user.uid
    session["valid_email"] = user.email
    return JSON.success(200)


def logout() -> dict:
    check_logged_in(loggedIn=False)

    session["logged_in"] = False
    return {"status": "ok", "message": "logged out successfully"}


def get_session() -> dict:
    return {
        "status": "ok",
        "session": dict(session),
    }


def check_logged_in(loggedIn: bool = True) -> None:
    if session.get("logged_in") if loggedIn else not session.get("logged_in"):
        JSONError.status_code = 409
        return JSONError.throw_json_error(
            error=f"Already logged {'in' if loggedIn else 'out'}"
        )
