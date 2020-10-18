from flask import request, jsonify
from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound, HTTPException

from ..service.kriteria_service import KriteriaService

api = Namespace("kriteria", "Endpoint untuk Kriteria")
DataKriteria = api.model(
    "kriteria",
    {
        "kode": fields.String(readonly=True),
        "nama": fields.String(
            required=True, description="Nama dari kriteria"
        ),
        "atribut": fields.String(
            required=True, description="Jenis atribut dari kriteria"
        ),
        "bobot": fields.Float(
            required=True,
            description="Bobot nilai dari setiap kriteria",
        ),
    },
)
kriteria = KriteriaService()


@api.route("/kriteria")
class KriteriaResourceAll(Resource):
    @api.doc(
        responses={200: "OK", 400: "Bad Request"},
        description="Endpoint untuk ambil data alternatif",
    )
    @api.marshal_list_with(DataKriteria, envelope="data")
    def get(self):
        try:
            return kriteria.GetAllData()
        except Exception as e:
            api.abort(400, e.__doc__)

    @api.doc(
        response={200: "OK", 500: "Internal Server Error"},
        description="Endpoint untuk menyimpan data kriteria",
    )
    @api.expect(DataKriteria)
    def post(self):
        try:
            GetDataFromJson = request.json
            KriteriaData = kriteria.AddKriteria(GetDataFromJson)
            return jsonify(KriteriaData)
        except HTTPException as e:
            api.abort(500, e)


@api.route("/kriteria/<kode>")
class KriteriaSpesificData(Resource):
    @api.doc(
        responses={200: "OK", 404: "Not Found"},
        description="Endpoint untuk ambil data kriteria spesifik",
    )
    @api.marshal_with(DataKriteria)
    def get(self, kode):
        KriteriaByKode = kriteria.GetSpesificData(kode)
        if not KriteriaByKode:
            api.abort(
                404,
                "Data Kriteria dengan kode {} tidak ditemukan".format(
                    kode
                ),
            )
        else:
            return KriteriaByKode

    @api.doc(responses={200: "OK", 404: "Not Found"})
    @api.expect(DataKriteria)
    def put(self, kode):
        print(api.payload)
        try:
            status, message = kriteria.UpdateData(kode, api.payload)
        except Exception as e:
            api.abort(400, e.__doc__)
        else:
            if status:
                return message
            else:
                return message
