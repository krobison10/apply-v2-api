import app.controllers.user_controller as user
from flask import Blueprint
from flask import jsonify


user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/user/<int:uid>', methods=['GET'])
def get_user_route(uid: int):
    return jsonify(user.get_user(uid=uid))


@user_routes.route('/users', methods=['GET'])
def get_all_users_route():
    return jsonify(user.get_all_users())

