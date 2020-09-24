from app.models.user_model import UserModel, RevokedTokenModel
from flask_jwt_extended import create_access_token, create_refresh_token


def LoginService(data):
    LoginData = UserModel.query.filter_by(username=data["username"]).first()
    if LoginData is None:
        message_object = {
            "status": "gagal",
            "message": "pengguna {} tidak terdaftar".format(data["username"]),
        }
        return message_object
    elif LoginData is not None and LoginData.verify_password(data["password"]):
        JwtAccessToken = create_access_token(identity=data["username"])
        RefreshToken = create_refresh_token(identity=data["username"])
        message_object = {
            "status": "berhasil",
            "message": "Pengguna {} berhasil login".format(data["username"]),
            "access_token": JwtAccessToken,
            "refresh_token": RefreshToken,
        }
        return message_object
    else:
        return {"status": "gagal", "message": "Kesalahan username atau password"}