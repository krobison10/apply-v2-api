from ..config import *


def get(aid: int) -> dict:
    Access.check_API_access()
    application = Application()
    application.uid = session["valid_uid"]
    application.aid = aid
    app_data = application.get()
    if not app_data:
        JSONError.status_code = 404
        JSONError.throw_json_error("Application not found")
    return app_data


def get_all() -> dict:
    Access.check_API_access()
    applications = Application()
    applications.uid = session["valid_uid"]
    application_results = applications.get_all()
    response = {"count": len(application_results), "results": application_results}
    return response


def create(data: dict) -> dict:
    Access.check_API_access()
    application = Application()
    application.uid = session["valid_uid"]

    Validate.required_fields(data, Application.required_fields, code=422)

    invalid_fields = []

    for field in data:
        if field in ["uid", "wage"]:
            Validate.number(data[field], field)
            setattr(application, field, int(data[field]))
        elif field in ["date", "job_start"]:
            # TODO: validation function for date
            try:
                setattr(application, field, datetime.strptime(data[field], "%Y-%m-%d"))
            except:
                JSONError.status_code = 422
                JSONError.throw_json_error(f"Field '{field}' must be a datetime")

        elif field in [
            "status",
            "resume",
            "cover_letter",
            "title",
            "description",
            "field",
            "position",
            "company",
            "industry",
            "website",
            "phone",
        ]:
            setattr(application, field, str(data[field]))
        else:
            invalid_fields.append(field)

    if invalid_fields:
        error = "Invalid fields supplied: " + implode(invalid_fields, ", ")
        JSONError.status_code = 422
        JSONError.throw_json_error(error)

    aid = application.save()

    response = JSON.success(201, {"aid": aid})
    return response


def edit(aid: int, data: dict) -> dict:
    Access.check_API_access()
    application = Application(session["valid_uid"], aid)

    invalid_fields = []

    for field in data:
        if field in ["uid", "wage"]:
            Validate.number(data[field], field)
            setattr(application, field, int(data[field]))
        elif field in ["date", "job_start"]:
            # TODO: validation function for date
            try:
                setattr(application, field, datetime.strptime(data[field], "%Y-%m-%d"))
            except:
                JSONError.status_code = 422
                JSONError.throw_json_error(f"Field '{field}' must be a datetime")

        elif field in [
            "status",
            "resume",
            "cover_letter",
            "title",
            "description",
            "field",
            "position",
            "company",
            "industry",
            "website",
            "phone",
        ]:
            setattr(application, field, str(data[field]))
        else:
            invalid_fields.append(field)

    if invalid_fields:
        error = "Invalid fields supplied: " + implode(invalid_fields, ", ")
        JSONError.status_code = 422
        JSONError.throw_json_error(error)

    application.save()

    response = JSON.success(200)
    return response


def delete(aid: int) -> bool:
    Access.check_API_access()
    application = Application()
    application.uid = session["valid_uid"]
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
