from app.models.user import User


def get_user(uid: int) -> dict:
    user = User()
    user.uid = uid
    user_data = user.get_user_by_id()
    return user_data


def get_all_users() -> dict:
    users = User().get_all_users()
    return users
