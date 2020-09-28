from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import datetime
import os


# inisialisasi db dan bcrypt
load_dotenv()
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_name):
    if config_name == "production":
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.getenv("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI_PROD"),
            SQLALCHEMY_TRACK_MODIFICATIONS=True,
            JWT_SECRET_KEY=os.getenv("JWT_KEY"),
            JWT_BLACKLIST_ENABLED=True,
            JWT_BLACKLIST_TOKEN_CHECKS=["access", "refresh"],
        )
        # Where to look for the JWT. Available options are cookies or headers
        app.config.setdefault("JWT_TOKEN_LOCATION", ("headers",))
        # Options for JWTs when the TOKEN_LOCATION is headers
        app.config.setdefault("JWT_HEADER_NAME", "Authorization")
        app.config.setdefault("JWT_HEADER_TYPE", "Bearer")
    else:
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.getenv("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI_DEV"),
            SQLALCHEMY_TRACK_MODIFICATIONS=True,
            JWT_SECRET_KEY=os.getenv("JWT_KEY"),
            JWT_BLACKLIST_ENABLED=True,
            JWT_BLACKLIST_TOKEN_CHECKS=["access", "refresh"],
        )
        # Where to look for the JWT. Available options are cookies or headers
        app.config.setdefault("JWT_TOKEN_LOCATION", ("headers",))
        # Options for JWTs when the TOKEN_LOCATION is headers
        app.config.setdefault("JWT_HEADER_NAME", "Authorization")
        app.config.setdefault("JWT_HEADER_TYPE", "Bearer")
    db.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)

    from app.models import user_model

    @jwt.token_in_blacklist_loader
    def CheckIfTokenInBlacklist(decrypted_token):
        jti = decrypted_token["jti"]
        return user_model.RevokedTokenModel.IsJtiBlackListed(jti)

    from .controller import controller as CtrlBlueprint

    app.register_blueprint(CtrlBlueprint, url_prefix="/api/v1")
    app.app_context().push()

    return app
