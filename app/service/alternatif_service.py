from ..models.alternatif_model import AlternatifModel
from app import db


def AddAlternatif(data):
    AlternatifData = AlternatifModel.query.filter_by(
        nama=data["nama"]
    ).first()
    if AlternatifData is None:
        try:
            SimpanAlternaitf = AlternatifModel(
                nim=data["nim"],
                nama=data["nama"],
                alamat=data["alamat"],
                jenis_kelamin=data["jenis_kelamin"],
            )
            db.session.add(SimpanAlternaitf)
            db.session.commit()
            message_object = {
                "status": "berhasil",
                "message": "{} berhasil ditambahkan kedalam alternatif".format(
                    data["nama"]
                ),
            }
            return message_object
        except Exception as e:
            db.session.rollback()
            message_object = {
                "status": "gagal",
                "message": "terjadi kesalahan saat menyimpan data",
            }
            return message_object
    else:
        message_object = {
            "status": "gagal",
            "message": "{} sudah terdaftar didalam alternatif".format(
                data["nama"]
            ),
        }
        return message_object


def GetAllAlternatif():
    return AlternatifModel.query.all()


def GetSpesificAlternatif(data):
    return AlternatifModel.query.filter_by(nim=data).first()
