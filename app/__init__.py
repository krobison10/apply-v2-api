from flask import Flask
from .services.routes import user_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_routes)
    return app