from flask import request, jsonify
from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound


from ..service.alternatif_service import AlternatifService

api = Namespace("alternatif", "Endpoint untuk Alternatif")
DataAlternatif = api.model(
    "alternatif",
    {
        "nim": fields.String(
            required=True,
            description="NIM mahasiswa yang ditambahkan kedalam alternatif",
        ),
        "nama": fields.String(
            required=True,
            description="Nama yang akan ditambahkan ke alternatif",
        ),
        "alamat": fields.String(
            required=True,
            description="Alamat dari altrnatif yang akan ditambahkan",
        ),
        "jenis_kelamin": fields.String(
            required=True,
            description="Jenis kelamin yang akan ditambahkan ke alternatif",
        ),
    },
)

alternatif = AlternatifService()


@api.route("/alternatif")
class AlternatifResourceAll(Resource):
    @jwt_required
    @api.doc(
        responses={200: "OK", 400: "Bad Request"},
        description="Endpoint untuk menyimpan data alternatif",
    )
    @api.expect(DataAlternatif)
    def post(self):
        try:
            GetAlternatifData = request.json
            AlternatifSatus = alternatif.AddAlternatif(GetAlternatifData)
            return jsonify(AlternatifSatus)
        except Exception as e:
            api.abort(400, e.__doc__)

    @jwt_required
    @api.doc(
        responses={200: "OK", 400: "Bad Request"},
        description="Endpoint untuk mengambil seluruh data alternatif",
    )
    @api.marshal_list_with(DataAlternatif, envelope="data")
    def get(self):
        try:
            return alternatif.GetAllData()
        except Exception as e:
            api.abort(404, e.__doc__)


@api.route("/alternatif/<nim>")
class AlternatifResourceByNIM(Resource):
    @jwt_required
    @api.doc(responses={200: "OK", 404: "Not Found"})
    @api.marshal_with(DataAlternatif)
    def get(self, nim):
        DataAlternatifByNim = alternatif.GetSpesificData(nim)
        if not DataAlternatifByNim:
            raise NotFound("Data alternatif tidak ditemukan")
        else:
            return DataAlternatifByNim

    @api.doc(responses={200: "OK", 404: "Not Found"})
    @api.expect(DataAlternatif)
    def put(self, nim):
        print(api.payload)
        try:
            status, message = alternatif.UpdateData(nim, api.payload)
        except Exception as e:
            api.abort(400, e.__doc__)
        else:
            if status:
                return message
            else:
                return message
