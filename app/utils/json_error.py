from flask import abort, jsonify


class JSONError:
    """
    Utility class for handling JSON-based error responses.
    """

    status_code = (
        500  # TODO: this persists between requests so we need to figure that out
    )

    # Predefined error types mapped to HTTP status codes.
    ERROR_TYPES = {
        400: "Bad Request",
        401: "Not Authorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        409: "Conflict",
        415: "Invalid Content Type",
        422: "Invalid Request",
        429: "Rate Limit Exceeded",
        500: "Internal Server Error",
    }

    @staticmethod
    def throw_json_error(error="", type=None):
        """
        Aborts the request and returns a JSON error response.

        Parameters:
        - error (str): The error message.
        - type (str, optional): The type of the error (e.g., 'warn'). Defaults to 'warn'.

        Returns:
        - None: Aborts the request with a JSON response.
        """
        response = {
            "code": JSONError.status_code,
            "error": JSONError.ERROR_TYPES[JSONError.status_code],
            "message": (error if error else "An error occurred"),
        }
        message = response["message"]
        response = jsonify(response)
        abort(JSONError.status_code, description=message)

    @staticmethod
    def logged_out():
        """
        Aborts the request and returns a 401 JSON error indicating the user is not logged in.

        Returns:
        - None: Aborts the request with a JSON response.
        """
        response = {
            "error": {
                "message": "You are not logged in, please log in and try again",
                "type": "warn",
            }
        }
        response = jsonify(response)
        abort(401, description="You are not logged in, please log in and try again")
