from flask import Flask, json
from flask_migrate import Migrate

from .extensions import db
from .routes import *


def register_blueprints(flask_app: Flask) -> None:
    blueprints = [
        link_with_github_bp,
        oauth_bp,
        github_bp
    ]

    for blueprint in blueprints:
        flask_app.register_blueprint(blueprint)


def set_app_config(flask_app: Flask) -> None:
    flask_app.config.from_file("config.json", load=json.load)
    flask_app.config.update(
        SQLALCHEMY_DATABASE_URI=flask_app.config.get('DATABASE_URI'),
    )


def create_app() -> Flask:
    flask_app = Flask(__name__)
    set_app_config(flask_app)
    db.init_app(flask_app)
    register_blueprints(flask_app)

    return flask_app


app = create_app()
migrate = Migrate(app, db)
