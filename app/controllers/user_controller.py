from ..config import *


def get(uid: int) -> dict:
    Access.check_API_access()
    user = User()
    user.uid = uid
    user_data = user.get_by_id()
    return user_data


# TODO: Remove this option maybe
def get_all() -> dict:
    Access.check_API_access()
    users = User().get_all()
    response = {"count": len(users), "results": users}
    return response
