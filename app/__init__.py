import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# blueprints
from .services.routes import server_routes
from .services.routes import user_routes
from .services.routes import auth_routes
from .services.routes import application_routes
from .services.routes import interview_routes


def create_app():
    app = Flask(__name__)
    
    app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    
    app.secret_key = os.getenv("SECRET_KEY")
    
    # blueprints    
    app.register_blueprint(server_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(application_routes)
    app.register_blueprint(interview_routes)
    
    return app
