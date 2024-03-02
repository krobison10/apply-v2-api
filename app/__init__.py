from werkzeug.exceptions import HTTPException
import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_mail import Mail

# blueprints
from .services.routes import server_routes
from .services.routes import user_routes
from .services.routes import auth_routes
from .services.routes import application_routes
from .services.routes import interview_routes

load_dotenv(find_dotenv())

error_codes = [
    400,
    401,
    403,
    404,
    405,
    406,
    408,
    409,
    410,
    411,
    412,
    413,
    414,
    415,
    416,
    417,
    418,
    422,
    423,
    424,
    428,
    429,
    431,
    451,
    500,
]

mail = Mail()


def create_app():
    app = Flask(__name__)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    app.secret_key = os.getenv("SECRET_KEY")

    # mail stuff
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = "kylerrobison8@gmail.com"
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False

    mail.init_app(app)

    @app.errorhandler(Exception)
    def handle_error(error):
        if hasattr(error, "code"):
            status_code = error.code
        else:
            status_code = 500
        response = jsonify(
            {
                "code": int(status_code),
                "error": (
                    error.name if hasattr(error, "name") else "Internal Server Error"
                ),
                "message": (
                    error.description
                    if hasattr(error, "description")
                    else str(error)  # Debug
                ),
            }
        )
        response.content_type = "application/json"

        return response, status_code

    for code in error_codes:
        app.register_error_handler(code, handle_error)

    # blueprints
    app.register_blueprint(server_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(application_routes)
    app.register_blueprint(interview_routes)

    return app
