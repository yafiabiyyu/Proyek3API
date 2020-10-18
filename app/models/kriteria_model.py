from app import db


class KriteriaModel(db.Model):
    __tablename__ = "kriteria"
    kode = db.Column(db.String(10), primary_key=True, autoincrement=False)
    nama = db.Column(db.String(50), nullable=False)
    atribut = db.Column(db.String(10), nullable=False)
    bobot = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "<Kriteria : {}>".format(self.nama)
