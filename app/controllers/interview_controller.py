from ..config import *


def get(iid: int) -> dict:
    Access.check_API_access()
    interview = Interview()
    interview.uid = session["valid_uid"]
    interview_data = interview.get(iid)
    if not interview_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Interview not found")
    return interview_data


def get_all() -> dict:
    Access.check_API_access()
    interview = Interview()
    interview.uid = session["valid_uid"]
    interview_results = interview.get_all()
    return interview_results
