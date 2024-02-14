from flask import Response
import json


class JSON:
    status_code = 200

    @staticmethod
    def success(code: int = 200, extra_fields: dict = None):
        response = {"code": code, "success": True}
        if extra_fields:
            response.update(extra_fields)
        return response

    @staticmethod
    def json_response(obj):
        response = Response(
            response=json.dumps(obj, default=str, sort_keys=False),
            status=JSON.status_code,
            mimetype="application/json",
        )
        return response
