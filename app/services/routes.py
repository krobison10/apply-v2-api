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


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":  # TODO: not this
        data = {}
        data["email"] = "Abby01@uw.edu"
        data["password"] = "password"
    else:
        data = request.json
    Validate.required_fields(data, ["email", "password"], code=422)
    result = auth_controller.login(data["email"], data["password"])
    return JSON.json_response(result)


@auth_routes.route("/logout", methods=["GET", "POST"])
def logout():
    return JSON.json_response(auth_controller.logout())


# endregion


# region: User routes


@user_routes.route("/user", methods=["GET", "PUT", "DELETE"])
def get_user_route():
    if request.method == "GET":
        return JSON.json_response(user_controller.get()), 200
    if request.method == "PUT":
        result = user_controller.update(request.json)
        return JSON.json_response(result), 200
    if request.method == "DELETE":
        result = user_controller.delete()
        return JSON.json_response(result), 200


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
            priority_filters = request.args.getlist("priority_filters")
            status_filters = request.args.getlist("status_filters")
            from_days_ago = request.args.get("from_days_ago")
            to_days_ago = request.args.get("to_days_ago")
            sort = request.args.get("sort")
            order = request.args.get("order")
            limit = request.args.get("limit")
            offset = request.args.get("offset")

            res = application_controller.get_all(
                priority_filters,
                status_filters,
                from_days_ago,
                to_days_ago,
                sort,
                order,
                limit,
                offset,
            )

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


@interview_routes.route("/interviews", methods=["GET", "POST", "PUT", "DELETE"])
def get_applications_route():
    if request.method == "GET":
        iid = request.args.get("iid")

        if iid:
            res = interview_controller.get(iid)
        else:
            application_filter_aid = (
                request.args.get("aid") if request.args.get("aid") else None
            )
            priority_filters = request.args.getlist("priority_filters")
            status_filters = request.args.getlist("status_filters")
            from_days_ago = request.args.get("from_days_ago")
            to_days_ago = request.args.get("to_days_ago")
            sort = request.args.get("sort")
            order = request.args.get("order")
            limit = request.args.get("limit")
            offset = request.args.get("offset")

            res = interview_controller.get_all(
                application_filter_aid,
                priority_filters,
                status_filters,
                from_days_ago,
                to_days_ago,
                sort,
                order,
                limit,
                offset,
            )

        return JSON.json_response(res), 200

    if request.method == "POST":
        result = interview_controller.create(request.json)
        return JSON.json_response(result), 201

    if request.method == "PUT":
        iid = request.args.get("iid")
        result = interview_controller.edit(iid, request.json)
        return JSON.json_response(result), 200

    if request.method == "DELETE":
        iid = request.args.get("iid")
        result = interview_controller.delete(iid)
        return JSON.json_response(result), 200


# endregion
