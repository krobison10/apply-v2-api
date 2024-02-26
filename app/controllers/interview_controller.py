from ..config import *


def get(iid: int) -> dict:
    Access.check_API_access()
    interview = Interview()
    interview.uid = session.get("valid_uid")
    interview.iid = iid
    interview_data = interview.get()
    if not interview_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Interview not found")
    return JSON.success(200, interview_data)


def get_all(
    application_filter_aid: int,
    priority_filters: list[str],
    status_filters: list[int],
    from_days_ago: int,
    to_days_ago: int,
    sort: str,
    order: str,
    limit: int,
    offset: int,
) -> dict:
    Access.check_API_access()
    limit = 100 if not limit else Validate.number(limit, "limit")
    offset = 0 if not offset else Validate.number(offset, "offset")

    from_days_ago = Validate.number(
        from_days_ago, "from_days_ago", required=False, positive=False
    )
    to_days_ago = Validate.number(
        to_days_ago, "to_days_ago", required=False, positive=False
    )

    limit = Validate.number(limit, "limit", required=False)
    offset = Validate.number(offset, "offset", required=False)

    interviews = Interviews()
    interviews.uid = session.get("valid_uid")
    interviews.aid = application_filter_aid

    interviews.set_priority_filters(priority_filters)
    interviews.set_status_filters(status_filters)
    interviews.set_date_filters(from_days_ago, to_days_ago)

    interviews.set_sort(sort)
    interviews.set_order(order)

    interviews.set_limit(limit)
    interviews.set_offset(offset)

    results = interviews.get()
    count = interviews.get(count=True)

    metadata = PaginateUtil.paginate(limit, offset, count, len(results))

    response = {
        "metadata": metadata,
        "results": results,
    }
    return JSON.success(200, response)


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
