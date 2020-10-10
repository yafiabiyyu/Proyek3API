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


def UpdateAlternatif(nim, data):
    GetData = AlternatifModel.query.get_or_404(nim)
    if GetData is not None:
        try:
            GetData.nim = data["nim"]
            GetData.nama = data["nama"]
            GetData.alamat = data["alamat"]
            GetData.jenis_kelamin = data["jenis_kelamin"]
            db.session.commit()
            message_object = {
                "status": "berhasil",
                "message": "data mahasiswa {} berhasil di perbarui".format(
                    data["nama"]
                ),
            }
            return True, message_object
        except Exception as e:
            db.session.rollback()
            message_object = {
                "status": "gagal",
                "message": "Terjadi kesalahan saat memperbarui data",
            }
            return False, message_object
    else:
        message_object = {
            "status": "gagal",
            "message": "Data tidak ditemukan",
        }
        return False, message_object
