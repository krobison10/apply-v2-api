# libraries
import config
from flask import Blueprint, request

# internal classes
from ..config import *

# blueprints, make sure to register in __init__.py
server_routes = Blueprint("server_routes", __name__)
auth_routes = Blueprint("auth_routes", __name__)
user_routes = Blueprint("user_routes", __name__)
application_routes = Blueprint("app_routes", __name__)
interview_routes = Blueprint("interview_routes", __name__)


# region: Server routes

@server_routes.route("/", methods=["GET"])
def index():
    response = {"name": "Apply V2 API", "version": config.API_VERSION}
    return JSON.json_response(response)

@auth_routes.route("/session", methods=["GET"])
def status():
    return JSON.json_response(auth.get_session())

#endregion


# region: Auth routes

@auth_routes.route("/login", methods=["GET"])
def login():
    if not request.args.get('uid'):
        JSONError.throw_json_error("Missing uid")
    uid = int(request.args.get('uid'))
    return JSON.json_response(auth.login(uid))


@auth_routes.route("/logout", methods=["GET"])
def logout():
    return JSON.json_response(auth.logout())
    
# endregion


# region: User routes

@user_routes.route("/user/<int:uid>", methods=["GET"])
def get_user_route(uid: int):
    return JSON.json_response(user.get(uid=uid))


@user_routes.route("/users", methods=["GET"])
def get_all_users_route():
    return JSON.json_response(user.get_all())

# endregion


# region: Application routes



# endregion


# region: Interview routes



# endregion
