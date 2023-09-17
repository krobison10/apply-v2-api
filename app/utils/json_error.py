from flask import abort, jsonify

class JSONError:
    """
    Utility class for handling JSON-based error responses.
    """
    
    status_code = 400

    # Predefined error types mapped to HTTP status codes.
    ERROR_TYPES = {
        400: 'bad_request',
        401: 'not_authorized',
        403: 'forbidden',
        404: 'not_found',
        405: 'method_not_allowed',
        409: 'conflict',
        415: 'invalid_content_type',
        422: 'invalid_request',
        429: 'rate_limit_exceeded',
        500: 'internal_server_error',
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
            'error': {
                'message': error if error else JSONError.ERROR_TYPES[JSONError.status_code], 
                'type': 'warn' if type is None else type
            }
        }
        message = response['error']['message']
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
            'error': {
                'message': "You are not logged in, please log in and try again", 
                'type': 'warn'
            }
        }
        response = jsonify(response)
        abort(401, description="You are not logged in, please log in and try again")
