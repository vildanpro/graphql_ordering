from logging import getLogger
from flask import json
from flask_restful import Api, Resource
from .models import Money
from .database import get_ranges_of_periods, get_suppliers, load_data_to_mongo


__all__ = ["create_api"]
__doc__ = "Information about api"

logger = getLogger('api')


def create_api(api=None):
    api = api if isinstance(api, Api) else Api(prefix='/v1')
    if getattr(api, '__created__', None):
        return api

    api.add_resource(GetSuppliers, '/get_suppliers/<int:cod_pl>', endpoint='get_suppliers')
    api.add_resource(GetPeriods, '/get_periods/<int:cod_pl>/<int:i_owner>', endpoint='get_periods')
    api.add_resource(GetPdf, '/get_periods/<int:cod_pl>/<int:i_owner>', endpoint='get_pdf')

    api.__created__ = True
    return api


class GetPdf(Resource):
    pass


class GetSuppliers(Resource):
    def get(self, cod_pl):
        return get_suppliers(cod_pl)


class GetPeriods(Resource):
    def get(self, cod_pl, i_owner):
        return get_ranges_of_periods(cod_pl=cod_pl, i_owner=i_owner)
