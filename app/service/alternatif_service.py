from ..models.alternatif_model import AlternatifModel
from app import db


class AlternatifService:
    def AddAlternatif(self, data):
        self.GetAlternatif = AlternatifModel.query.filter_by(
            nama=data["nama"]
        ).first()
        if self.GetAlternatif is None:
            try:
                self.SaveAlternatif = AlternatifModel(
                    nim=data["nim"],
                    nama=data["nama"],
                    alamat=data["alamat"],
                    jenis_kelamin=data["jenis_kelamin"],
                )
                db.session.add(self.SaveAlternatif)
                db.session.commit()
                self.message_object = {
                    "status": "berhasil",
                    "message": "Alternatif {} berhasil ditambahkan".format(
                        data["nama"]
                    ),
                }
                return self.message_object
            except Exception as e:
                db.session.rollback()
                self.message_object = {
                    "status": "gagal",
                    "message": "Alternatif {} gagal ditambahkan".format(
                        data["nama"]
                    ),
                }
        else:
            self.message_object = {
                "status": "gagal",
                "message": "Alternatif {} telah terdaftar".format(
                    data["nama"]
                ),
            }
            return self.message_object

    def GetAllData(self):
        return AlternatifModel.query.all()

    def GetSpesificData(self, data):
        return AlternatifModel.query.filter_by(nim=data).first()

    def UpdateData(self, nim, data):
        self.GetData = AlternatifModel.query.get_or_404(nim)
        if self.GetData is not None:
            try:
                self.GetData.nim = data["nim"]
                self.GetData.nama = data["nama"]
                self.GetData.alamat = data["alamat"]
                self.GetData.jenis_kelamin = data["jenis_kelamin"]
                db.session.commit()
                self.message_object = {
                    "status": "berhasil",
                    "message": "Data {} berhasil di perbarui".format(
                        data["nama"]
                    ),
                }
                return True, self.message_object
            except Exception as e:
                db.session.rollback()
                self.message_object = {
                    "status": "gagal",
                    "message": "Terjadi kesalahan saat memperbarui data",
                }
                return False, self.message_object
        else:
            self.message_object = {
                "status": "gagal",
                "message": "Data {} tidak ditemukan dalam database".format(
                    data["nama"]
                ),
            }
            return False, self.message_object
