from ..config import *


def get(aid: int) -> dict:
    Access.check_API_access()
    application = Application()
    application.uid = session.get("valid_uid")
    application.aid = aid
    app_data = application.get()
    if not app_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Application not found")
    return app_data


def get_all() -> dict:
    Access.check_API_access()
    applications = Application()
    applications.uid = session.get("valid_uid")
    application_results = applications.get_all()
    response = {"count": len(application_results), "results": application_results}
    return response


def validate_application_fields(application, data):
    invalid_fields = []

    for field in data:
        if field in ["uid", "aid", "position_wage", "priority"]:
            Validate.number(data[field], field)
            setattr(application, field, int(data[field]))
        elif field in ["application_date", "job_start"]:
            # TODO: validation function for date
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

    if invalid_fields:
        error = "Invalid fields supplied: " + implode(invalid_fields, ", ")
        JSONError.status_code = 422
        JSONError.throw_json_error(error)


def create(data: dict) -> dict:
    Access.check_API_access()
    application = Application()
    application.uid = session.get("valid_uid")

    Validate.required_fields(data, Application.required_fields, code=422)

    validate_application_fields(application, data)

    aid = application.save()

    response = JSON.success(201, {"aid": aid})
    return response


def edit(aid: int, data: dict) -> dict:
    Access.check_API_access()
    application = Application(session.get("valid_uid"), aid)

    validate_application_fields(application, data)

    application.save()

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
