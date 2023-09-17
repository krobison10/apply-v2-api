from ..config import *

def get(uid: int) -> dict:
    Access.check_API_access()
    user = User()
    user.uid = uid
    user_data = user.get_by_id()
    return user_data


def get_all() -> dict:
    Access.check_API_access()
    users = User().get_all()
    return users
