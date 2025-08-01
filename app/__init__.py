from flask import Flask
from config import Config
from app.extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import tickets

    app.register_blueprint(tickets.bp)

    from app import models

    with app.app_context():
        db.create_all()

    return app

