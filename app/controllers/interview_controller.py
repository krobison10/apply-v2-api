from ..config import *


def get(iid: int, expand: bool = False) -> dict:
    Access.check_API_access()
    interview = Interview()
    interview.uid = session.get("valid_uid")
    interview.iid = iid
    interview_data = interview.get(expand)
    if not interview_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Interview not found")
    return interview_data


def get_all(expand: bool = False) -> dict:
    Access.check_API_access()
    interview = Interview()
    interview.uid = session.get("valid_uid")
    interview_results = interview.get_all(expand)
    response = {"count": len(interview_results), "results": interview_results}
    return response


def validate_interview_fields(interview, data):
    invalid_fields = []

    for field in data:
        if field in ["iid", "aid"]:
            Validate.number(data[field], field)
            setattr(interview, field, int(data[field]))
        elif field in ["date"]:
            # TODO: validation function for date
            try:
                setattr(interview, field, parser.parse(data[field]))
            except:
                invalid_fields.append(field)

        elif field in ["modality", "location", "notes", "type"]:
            setattr(interview, field, str(data[field]))
        else:
            invalid_fields.append(field)

    if invalid_fields:
        error = "Invalid fields supplied: " + implode(invalid_fields, ", ")
        JSONError.status_code = 422
        JSONError.throw_json_error(error)


def create(data: dict) -> dict:
    Access.check_API_access()
    interview = Interview()
    interview.uid = session.get("valid_uid")

    if "iid" in data:
        JSONError.status_code = 422
        JSONError.throw_json_error("IID cannot be supplied for new interview")

    Validate.required_fields(data, Interview.required_fields, code=422)

    validate_interview_fields(interview, data)  # sets the aid

    iid = interview.save()

    response = JSON.success(201, {"iid": iid})
    return response


def edit(iid: int, data: dict) -> dict:
    Access.check_API_access()
    interview = Interview()
    interview.uid = session.get("valid_uid")
    interview.iid = iid

    interview_data = interview.get()
    if not interview_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Interview not found")

    interview.set(interview_data)

    validate_interview_fields(interview, data)

    iid = interview.save()

    response = JSON.success(200)
    return response


def delete(iid: int) -> bool:
    Access.check_API_access()
    interview = Interview()
    interview.uid = session.get("valid_uid")
    interview.iid = iid

    interview_data = interview.get()
    if not interview_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Interview not found")

    rows_affected = interview.delete()

    if not rows_affected:
        JSONError.status_code = 500
        JSONError.throw_json_error("Failed to delete interview")

    response = JSON.success(200)
    return response
