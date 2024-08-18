from flask import Flask, send_from_directory
from flask_cors import CORS
from .dash_app import create_dash_app
import os

# added for the DB connection
from .routes import generate as generate_blueprint
from .routes import main as main_blueprint


# This function is responsible for creating and configuring the Flask application.

def create_app():
    # Instantiate the Flask application with the given static and template folders
    app = Flask(__name__, static_folder='../frontend/dist', template_folder='../frontend/dist')
    # Enable Cross-Origin Resource Sharing (CORS) to allow requests from different origins
    CORS(app, supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])

    # Initialize and integrate the Dash application with the Flask app
    dash_app = create_dash_app(app)

    # Register blueprints for different parts of the application
    # `generate_blueprint` handles routes prefixed with '/generate'
    app.register_blueprint(generate_blueprint, url_prefix='/generate')

    # `main_blueprint` handles other routes, no prefix is used
    app.register_blueprint(main_blueprint)

    # Define a route to serve static files or the main index file
    # The route handles both the root ('/') and any other path ('/<path:path>')
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        # If the requested path is not empty and the file exists in the static folder, serve it
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    # Return the configured Flask app instance
    return app
