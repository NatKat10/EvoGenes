from flask import Flask, send_from_directory
from .extensions import db, ma
from flask_cors import CORS
from .dash_app import create_dash_app
import os

def create_app():
    app = Flask(__name__, static_folder='../frontend/dist', template_folder='../frontend/dist')
    CORS(app)

    # Initialize Dash app
    dash_app = create_dash_app(app)  

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # db.init_app(app)
    ma.init_app(app)

    from .routes import generate as generate_blueprint
    from .routes import main as main_blueprint

    app.register_blueprint(generate_blueprint, url_prefix='/generate')
    app.register_blueprint(main_blueprint)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app
