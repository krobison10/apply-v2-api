from ..config import *
from random import randint
from flask_mail import Message


def login(email: str, password: str) -> dict:
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

    onboard = False
    if not user_data or user_data["email_verified"] == 0:
        onboard = True

    # success
    session["logged_in"] = True
    session["valid_uid"] = user.uid
    session["valid_email"] = user.email

    if not user_data:
        create_activation()

    return JSON.success(200, {"onboard": onboard})


def logout() -> dict:
    session["logged_in"] = False
    return {"status": "ok", "message": "logged out successfully"}


def send_activation(email, code) -> dict:
    from .. import mail

    msg = Message(
        "Verify your new Account", sender="kylerrobison8@gmail.com", recipients=[email]
    )
    msg.body = f"Your verification code is: {code}. \n\n I was too lazy to create a new email account for this."
    mail.send(msg)


def create_activation() -> dict:
    user = User(session.get("valid_uid"))

    if user.email_verified:
        JSONError.status_code = 409
        return JSONError.throw_json_error("Already activated")

    code = randint(100000, 999999)

    user.create_activation(code)

    send_activation(user.email, code)

    return JSON.success(201)


def activate(data: dict) -> dict:
    user = User(session.get("valid_uid"))

    code = Validate.number(data["code"], "code")

    if user.email_verified:
        JSONError.status_code = 409
        return JSONError.throw_json_error("Already activated")

    activation = user.get_activation()
    if not activation:
        JSONError.status_code = 404
        return JSONError.throw_json_error("Activation not found")

    if activation["code"] != code:
        JSONError.status_code = 422
        return JSONError.throw_json_error("Invalid activation code")

    user.email_verified = 1
    user.save()

    user.delete_activation()

    return JSON.success(200)


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
