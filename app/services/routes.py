import config
import app.controllers.user_controller as user
from flask import Blueprint
from flask import jsonify


app_routes = Blueprint("app_routs", __name__)


@app_routes.route("/", methods=["GET"])
def index():
    response = {"name": "Apply V2 API", "version": config.API_VERSION}
    return jsonify(response)


user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/user/<int:uid>", methods=["GET"])
def get_user_route(uid: int):
    return jsonify(user.get_user(uid=uid))


@user_routes.route("/users", methods=["GET"])
def get_all_users_route():
    return jsonify(user.get_all_users())
