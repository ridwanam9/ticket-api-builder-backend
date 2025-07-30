# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from config import Config

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     db.init_app(app)

#     from app.routes import users, products, transactions
#     app.register_blueprint(users.bp)
#     app.register_blueprint(products.bp)
#     app.register_blueprint(transactions.bp)

#     with app.app_context():
#         db.create_all()

#     return app

from flask import Flask
from config import Config
from app.extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import users, products, transactions
    app.register_blueprint(users.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(transactions.bp)

    from app import models

    with app.app_context():
        db.create_all()

    return app

