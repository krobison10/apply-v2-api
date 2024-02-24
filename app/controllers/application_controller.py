from ..config import *
import base64
import uuid


def get(aid: int) -> dict:
    Access.check_API_access()
    application = Application()
    application.uid = session.get("valid_uid")
    application.aid = aid
    app_data = application.get()
    if not app_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Application not found")
    # TODO: embed application in object
    return JSON.success(200, app_data)


def get_all(
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

    applications = Applications()
    applications.uid = session.get("valid_uid")

    applications.set_priority_filters(priority_filters)
    applications.set_status_filters(status_filters)
    applications.set_date_filters(from_days_ago, to_days_ago)

    applications.set_sort(sort)
    applications.set_order(order)

    applications.set_limit(limit)
    applications.set_offset(offset)

    results = applications.get()
    count = applications.get(count=True)

    metadata = PaginateUtil.paginate(limit, offset, count, len(results))

    response = {
        "metadata": metadata,
        "results": results,
    }
    return JSON.success(200, response)


def validate_application_fields(application, data):
    invalid_fields = []

    for field in data:
        if field in ["uid", "aid", "position_wage", "priority"]:
            Validate.number(data[field], field, required=False)
            setattr(application, field, int(data[field]))
        elif field in ["application_date", "job_start"]:
            try:
                setattr(application, field, parser.parse(data[field]))
            except:
                invalid_fields.append(field)

        elif field in [
            "status",
            "resume_url",
            "cover_letter_url",
            "position_title",
            "notes",
            "position_level",
            "company_name",
            "company_industry",
            "company_website",
            "posting_url",
            "job_location",
            "posting_source",
            "priority",
        ]:
            setattr(application, field, str(data[field]))
        else:
            invalid_fields.append(field)

        if field == "status" and data[field] not in Application.valid_statuses:
            invalid_fields.append(field)

        if (
            field == "priority"
            and data[field] not in Application.valid_priorities_map.keys()
            and data[field] not in Application.valid_priorities_map.values()
        ):
            invalid_fields.append(field)

    if invalid_fields:
        error = "Invalid fields supplied: " + implode(invalid_fields, ", ")
        JSONError.status_code = 422
        JSONError.throw_json_error(error)


def upload_application_doc(file) -> str:
    extension = file.split(";")[0].split("/")[1]
    file = file.split(",")[1] + "==="
    name = str(uuid.uuid4()) + "." + extension
    file_bytes = base64.b64decode(file)
    object_url = AWS.s3_upload_file("applyapp.applications.documents", name, file_bytes)
    return object_url


def create(data: dict) -> dict:
    Access.check_API_access()
    application = Application()
    application.uid = session.get("valid_uid")

    Validate.required_fields(data, Application.required_fields, code=422)

    if "resume" in data and data["resume"]:
        resume_url = upload_application_doc(data["resume"])
        data["resume_url"] = resume_url

    if "cover_letter" in data and data["cover_letter"]:
        cover_letter_url = upload_application_doc(data["cover_letter"])
        data["cover_letter_url"] = cover_letter_url

    del data["resume"]
    del data["cover_letter"]

    validate_application_fields(application, data)

    aid = application.save()

    if not aid:
        JSONError.status_code = 500
        JSONError.throw_json_error("Failed to create application")

    response = JSON.success(201, {"aid": aid})
    return response


def edit(aid: int, data: dict) -> dict:
    Access.check_API_access()

    application = Application()
    application.uid = session.get("valid_uid")
    application.aid = aid

    app_data = application.get()
    if not app_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Application not found")

    application.set(app_data)

    if "resume" in data and data["resume"]:
        resume_url = upload_application_doc(data["resume"])
        data["resume_url"] = resume_url

    if "cover_letter" in data and data["cover_letter"]:
        cover_letter_url = upload_application_doc(data["cover_letter"])
        data["cover_letter_url"] = cover_letter_url

    del data["resume"]
    del data["cover_letter"]

    validate_application_fields(application, data)

    id = application.save()

    if not aid:
        JSONError.status_code = 500
        JSONError.throw_json_error("Failed to update application")

    response = JSON.success(200)
    return response


def delete(aid: int) -> bool:
    Access.check_API_access()
    application = Application()
    application.uid = session.get("valid_uid")
    application.aid = aid

    app_data = application.get()
    if not app_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Application not found")

    rows_affected = application.delete()

    if not rows_affected:
        JSONError.status_code = 500
        JSONError.throw_json_error("Failed to delete application")

    response = JSON.success(200)
    return response
