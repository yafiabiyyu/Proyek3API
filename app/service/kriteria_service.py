from ..models.kriteria_model import KriteriaModel
from app import db
from uuid import uuid4


class KriteriaService:
    def AddKriteria(self, data):
        self.GetKriteriaData = KriteriaModel.query.filter_by(
            nama=data["nama"]
        ).first()
        if self.GetKriteriaData is None:
            try:
                self.SaveKriteriaData = KriteriaModel(
                    kode=str(uuid4())[:8],
                    nama=data["nama"],
                    atribut=data["atribut"],
                    bobot=float(data["bobot"]),
                )
                db.session.add(self.SaveKriteriaData)
                db.session.commit()
                self.message_object = {
                    "status": "berhasil",
                    "message": "Data Kriteria {} berhasil ditambahkan".format(
                        data["nama"]
                    ),
                }
                return self.message_object
            except Exception as e:
                db.session.rollback()
                self.message_object = {
                    "status": "gagal",
                    "message": "Data Kriteria {} gagal ditambahkan".format(
                        data["nama"]
                    ),
                }
                return self.message_object
        else:
            self.message_object = {
                "status": "gagal",
                "message": "Data Kriteria {} telah terdaftar".format(
                    data["nama"]
                ),
            }
            return self.message_object

    def UpdateData(self, kode, data):
        self.GetData = KriteriaModel.query.get_or_404(kode)
        if self.GetData is not None:
            try:
                self.GetData.kode = data["kode"]
                self.GetData.nama = data["nama"]
                self.GetData.atribut = data["atribut"]
                self.GetData.bobot = data["bobot"]
                db.session.commit()
                self.message_object = {
                    "status": "berhasil",
                    "message": "Kriteria {} berhasil diperbarui".format(
                        data["nama"]
                    ),
                }
                return True, self.message_object
            except Exception as e:
                db.session.rollback()
                self.message_object = {
                    "status": "berhasil",
                    "message": "Kriteria {} gagal diperbarui".format(
                        data["nama"]
                    ),
                }
                return False, self.message_object

    def GetAllData(self):
        return KriteriaModel.query.all()

    def GetSpesificData(self, kode):
        return KriteriaModel.query.filter_by(kode=kode).first()
