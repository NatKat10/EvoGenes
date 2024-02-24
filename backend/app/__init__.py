from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__, static_folder='../../frontend/dist', static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ayenat1@localhost/mydb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        from .routes import main as routes_main
        app.register_blueprint(routes_main)
        db.create_all()

    return app