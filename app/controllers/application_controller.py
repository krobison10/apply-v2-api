from ..config import *


def get(aid: int, expand: bool = False) -> dict:
    Access.check_API_access()
    application = Application()
    application.uid = session["valid_uid"]
    app_data = application.get(aid, expand)
    if not app_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Application not found")
    return app_data


def get_all(expand: bool = False) -> dict:
    Access.check_API_access()
    applications = Application()
    applications.uid = session["valid_uid"]
    application_results = applications.get_all(expand)
    response = {"count": len(application_results), "results": application_results}
    return response
