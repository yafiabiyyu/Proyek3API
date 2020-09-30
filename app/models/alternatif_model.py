from app import db
from enum import Enum


class JenisKelaminType(Enum):
    laki = "Laki-Laki"
    perempuan = "Perempuan"


class AlternatifModel(db.Model):
    __tablename__ = "alternatif"
    nim = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nama = db.Column(db.String(50), nullable=False)
    alamat = db.Column(db.String(100), nullable=False)
    jenis_kelamin = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "<Alternatif : {}>".format(self.nama)
