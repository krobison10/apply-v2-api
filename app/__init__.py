from flask import Flask
from .services.routes import user_routes
from .services.routes import app_routes


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_routes)
    app.register_blueprint(app_routes)
    return app
