import os

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from blocklist import BLOCKLIST

from ressources.item import blp as ItemBlueprint
from ressources.store import blp as StoreBlueprint
from ressources.tag import blp as TagBlueprint
from ressources.user import blp as UserBlueprint

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores Rest API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)
    app.config["JWT_SECRET_KEY"] = "123853720532633570538762837813013483418"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def token_in_blocklist_loader(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_loader(jwt_header, jwt_payload):
        return {
            "description": "The token has been revoked",
            "error": "token_revoked",
        }, 401

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_loader(jwt_header, jwt_payload):
        return {
            "description": "The token is not fresh",
            "error": "fresh_token_required",
        }, 401

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_loader(jwt_header, jwt_payload):
        return {"message": "The token has expired.", "error": "token_expired"}, 401

    @jwt.invalid_token_loader
    def invalid_token_loader(error):
        return {
            "message": "Signature verification failed.",
            "error": "invalid_token",
        }, 401

    @jwt.unauthorized_loader
    def unauthorized_loader(error):
        return {
            "message": "Request does not contain an access token.",
            "error": "authorization_required",
        }, 401

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
