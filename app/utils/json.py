from flask import Response
import json


class JSON:
    status_code = 200

    @staticmethod
    def json_response(obj):
        response = Response(
            response=json.dumps(obj, default=str, sort_keys=False),
            status=JSON.status_code,
            mimetype="application/json",
        )
        return response
