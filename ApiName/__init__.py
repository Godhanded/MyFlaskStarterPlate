from flask_limiter.util import get_remote_address
from ApiName.config import App_Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_limiter import Limiter
from flask import Flask, session
from flask_caching import Cache
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_cors import CORS
import os


db = SQLAlchemy()

bcrypt = Bcrypt()

sess = Session()

mail = Mail()

cache = Cache()


def create_app(config_class=App_Config):
    """
    Create a new instance of the app with the given configuration.

    :param config_class: configuration class
    :return: app
    """
    # Initialize Flask-
    app = Flask(__name__)
    app.config["SESSION_SQLALCHEMY"] = db
    app.config.from_object(App_Config)
    # Initialize CORS
    CORS(app, supports_credentials=True)
    # Initialize SQLAlchemy
    db.init_app(app)
    # Initialize Flask-Mail
    mail.init_app(app)
    # Initialize Bcrypt
    bcrypt.init_app(app)
    # Initialize Flask-Session
    sess.init_app(app)
    migrate = Migrate(app, db)
    # Initialize cache
    cache.init_app(app)

    from ApiName.auth.routes import auth
    from ApiName.errors.handlers import error

    app.register_blueprint(auth)
    app.register_blueprint(error)

    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=["2 per second", "200 per day", "50 per hour"],
        storage_uri=os.environ.get("REDIS"),
    )

    # with app.app_context():
    #     db.create_all()

    return app
