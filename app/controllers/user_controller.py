from ..config import *


def get() -> dict:
    Access.check_API_access()
    user = User()
    user.uid = session["valid_uid"]
    user_data = user.get_by_id()
    if not user_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("User not found")
    return user_data


# TODO: Remove this option maybe
def get_all() -> dict:
    Access.check_API_access()
    users = User().get_all()
    response = {"count": len(users), "results": users}
    return response


def update(data: dict) -> dict:
    Access.check_API_access()
    user = User(session["valid_uid"])
    user.set(data)
    user.save()
    response = JSON.success(200)
    return response


def delete() -> dict:
    Access.check_API_access()
    user = User(session["valid_uid"])
    user.delete()

    session["logged_in"] = False
    session["valid_uid"] = None
    response = JSON.success(200)

    return response
