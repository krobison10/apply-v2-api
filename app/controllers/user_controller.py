from app.models.user import User

def get_user(user_id):
    user = User().get_user_by_id(user_id)
    return user


def get_all_users():
    users = User().get_all_users()
    return users