from app.controllers.user_controller import get_user
from flask import Blueprint

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/user/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    return get_user(user_id)


