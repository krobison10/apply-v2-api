# libraries
import config
from flask import Blueprint

# internal classes
from ..config import *

# blueprints, !!! make sure to register in __init__.py !!!
server_routes = Blueprint("server_routes", __name__)
auth_routes = Blueprint("auth_routes", __name__)
user_routes = Blueprint("user_routes", __name__)
application_routes = Blueprint("application_routes", __name__)
interview_routes = Blueprint("interview_routes", __name__)


# region: Server routes


@server_routes.route("/", methods=["GET"])
def index():
    response = {"name": "Apply V2 API", "version": config.API_VERSION}
    return JSON.json_response(response)


@auth_routes.route("/session", methods=["GET"])
def status():
    return JSON.json_response(auth_controller.get_session())


# endregion


# region: Auth routes


@auth_routes.route("/login", methods=["GET"])
def login():
    if not request.args.get("uid"):
        JSONError.status_code = 422
        JSONError.throw_json_error("Missing uid")
    uid = int(request.args.get("uid"))
    return JSON.json_response(auth_controller.login(uid))


@auth_routes.route("/logout", methods=["GET"])
def logout():
    return JSON.json_response(auth_controller.logout())


# endregion


# region: User routes


@user_routes.route("/user/<int:uid>", methods=["GET"])
def get_user_route(uid: int):
    return JSON.json_response(user_controller.get(uid=uid)), 200


@user_routes.route("/users", methods=["GET"])
def get_all_users_route():
    return JSON.json_response(user_controller.get_all()), 200


# endregion


# region: Application routes


@application_routes.route("/applications", methods=["GET", "POST", "PUT", "DELETE"])
def applications_routes():
    if request.method == "GET":
        aid = request.args.get("aid")

        if aid:
            res = application_controller.get(aid)
        else:
            res = application_controller.get_all()

        return JSON.json_response(res), 200

    if request.method == "POST":
        result = application_controller.create(request.json)
        return JSON.json_response(result), 201

    if request.method == "PUT":
        aid = request.args.get("aid")
        result = application_controller.edit(aid, request.json)
        return JSON.json_response(result), 200

    if request.method == "DELETE":
        aid = request.args.get("aid")
        result = application_controller.delete(aid)
        return JSON.json_response(result), 200


# endregion


# region: Interview routes


@interview_routes.route("/interviews", methods=["GET"])
def get_applications_route():
    expand = request.args.get("expand")
    expand = True if expand == "true" else False

    iid = request.args.get("iid")
    if iid:
        res = interview_controller.get(iid, expand)
    else:
        res = interview_controller.get_all(expand)

    return JSON.json_response(res)


# endregion
