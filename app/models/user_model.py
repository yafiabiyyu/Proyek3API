from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = "user_model"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    paswword_hash = db.Column(db.String(128))

    def saveToDb(self):
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError("Kata sandi bukanlah atribut yag dapat dibaca")

    @password.setter
    def password(self, password):
        # merubah password ke password hash
        self.paswword_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.paswword_hash, password)

    def __repr__(self):
        return "<UserModel: {}>".format(self.username)


class RevokedTokenModel(db.Model):
    __tablename__ = "revoked_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def saveToDb(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def IsJtiBlackListed(cls, jti):
        Query = cls.query.filter_by(jti=jti).first()
        return bool(Query)
