from ..config import *
import base64
import secrets
import string


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
    search_term: str,
    priority_filters: list[str],
    status_filters: list[int],
    from_days_ago: int,
    to_days_ago: int,
    show_archived: bool,
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
    applications.show_archived = show_archived

    applications.set_search_term(search_term.strip() if search_term else search_term)

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


def handle_upload_docs(data: dict) -> dict:
    if (
        "resume" in data
        and data["resume"]
        and "resume_name" in data
        and data["resume_name"]
    ):
        resume_url = upload_application_doc(data["resume"], data["resume_name"])
        data["resume_url"] = resume_url

    if (
        "cover_letter" in data
        and data["cover_letter"]
        and "cover_letter_name" in data
        and data["cover_letter_name"]
    ):
        cover_letter_url = upload_application_doc(
            data["cover_letter"], data["cover_letter_name"]
        )
        data["cover_letter_url"] = cover_letter_url

    if "resume" in data:
        del data["resume"]
    if "resume_name" in data:
        del data["resume_name"]
    if "cover_letter" in data:
        del data["cover_letter"]
    if "cover_letter_name" in data:
        del data["cover_letter_name"]


def upload_application_doc(file, name) -> str:
    extension = file.split(";")[0].split("/")[1]
    file = file.split(",")[1] + "==="

    random_string = "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(8)
    )
    name = name.split(".")[0] + "-" + random_string + "." + extension

    file_bytes = base64.b64decode(file)
    object_url = AWS.s3_upload_file("applyapp.applications.documents", name, file_bytes)
    return object_url


def delete_application_doc(url: str) -> bool:
    name = url.replace(
        "https://applyapp.applications.documents.s3-us-west-2.amazonaws.com/", ""
    )
    AWS.s3_delete_file("applyapp.applications.documents", name)
    return True


def create(data: dict) -> dict:
    Access.check_API_access()
    application = Application()
    application.uid = session.get("valid_uid")

    Validate.required_fields(data, Application.required_fields, code=422)

    handle_upload_docs(data)

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

    handle_upload_docs(data)
    # TODO: delete old s3 doc if new one uploaded

    validate_application_fields(application, data)

    id = application.save()

    if not aid:
        JSONError.status_code = 500
        JSONError.throw_json_error("Failed to update application")

    response = JSON.success(200)
    return response


def pin(aid: int, data: dict) -> dict:
    Access.check_API_access()
    application = Application()
    application.uid = session.get("valid_uid")
    application.aid = aid

    if "pinned" not in data:
        JSONError.status_code = 422
        JSONError.throw_json_error("'pinned' field is required")

    pinned = Validate.number(data["pinned"], "pinned")

    app_data = application.get()
    if not app_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Application not found")

    application.pinned = pinned

    rows_affected = application.pin()

    if not rows_affected:
        JSONError.status_code = 500
        JSONError.throw_json_error("Failed to update application")

    response = JSON.success(200)
    return response


def archive(aid: int, data: dict) -> dict:
    Access.check_API_access()
    application = Application()
    application.uid = session.get("valid_uid")
    application.aid = aid

    if "archived" not in data:
        JSONError.status_code = 422
        JSONError.throw_json_error("'archived' field is required")

    archived = Validate.number(data["archived"], "archived")

    app_data = application.get()
    if not app_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Application not found")

    application.archived = archived

    rows_affected = application.archive()

    if not rows_affected:
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

    # TODO: cron to delete docs for deleted accounts
    if app_data["resume_url"]:
        delete_application_doc(app_data["resume_url"])

    if app_data["cover_letter_url"]:
        delete_application_doc(app_data["cover_letter_url"])

    rows_affected = application.delete()

    if not rows_affected:
        JSONError.status_code = 500
        JSONError.throw_json_error("Failed to delete application")

    response = JSON.success(200)
    return response
