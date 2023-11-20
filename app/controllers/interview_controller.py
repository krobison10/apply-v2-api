from ..config import *


def get(iid: int, expand: bool = False) -> dict:
    Access.check_API_access()
    interview = Interview()
    interview.uid = session["valid_uid"]
    interview_data = interview.get(iid, expand)
    if not interview_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Interview not found")
    return interview_data


def get_all(expand: bool = False) -> dict:
    Access.check_API_access()
    interview = Interview()
    interview.uid = session["valid_uid"]
    interview_results = interview.get_all(expand)
    return interview_results
