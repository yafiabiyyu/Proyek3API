from flask import request, jsonify
from flask_restplus import Resource, Namespace, fields
from werkzeug.exceptions import NotFound
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)
from ..service.auth_service import LoginService
from ..models.user_model import RevokedTokenModel


api = Namespace("login", "Endpoint API untuk login")
DataLogin = api.model(
    "login",
    {
        "username": fields.String(
            required=True,
            description="Username user yang akan menggunakan aplikasi",
        ),
        "password": fields.String(
            required=True,
            description="Password user yang akan menggunakan aplikasi",
        ),
    },
)


@api.route("/login")
class LoginResource(Resource):
    @api.doc(
        responses={200: "OK", 400: "Bad Request"},
        description="Endpoint untuk login",
    )
    @api.expect(DataLogin)
    def post(self):
        try:
            GetUserData = request.json
            LoginStatus = LoginService(GetUserData)
            return jsonify(LoginStatus)
        except Exception as e:
            api.abort(400, e.__doc__)


@api.route("/token/refresh")
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        CurrentUser = get_jwt_identity()
        NewAccessToken = create_access_token(identity=CurrentUser)
        return jsonify({"access_token": NewAccessToken})


@api.route("/logout")
class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        try:
            RevokedToken = RevokedTokenModel(jti=jti)
            RevokedToken.saveToDb()
            return jsonify(
                {
                    "status": "berhasil",
                    "message": "user berhasil logout",
                }
            )
        except Exception:
            return jsonify(
                {"status": "gagal", "message": "terjadi kesalahan"}
            )
