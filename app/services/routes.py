from app.controllers.user_controller import *
from flask import Blueprint
from flask import jsonify


user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/user/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    return get_user(user_id)


@user_routes.route('/users', methods=['GET'])
def get_all_users_route():
    return jsonify(get_all_users())

