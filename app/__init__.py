import os
from flask import Flask

# blueprints
from .services.routes import user_routes
from .services.routes import auth_routes
from .services.routes import app_routes


def create_app():
    app = Flask(__name__)
    
    app.secret_key = os.getenv("SECRET_KEY")
    
    # blueprints    
    app.register_blueprint(user_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(app_routes)
    return app
