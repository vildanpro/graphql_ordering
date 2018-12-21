from logging import getLogger
from pprint import pprint
from flask_restful import Api, Resource
from .models import Money
from .database import load_data_to_mongo, get_periods, get_suppliers

__all__ = ["create_api"]
__doc__ = "Information about api"

logger = getLogger('api')


def create_api(api=None):
    api = api if isinstance(api, Api) else Api(prefix='/v1')
    if getattr(api, '__created__', None):
        return api

    api.add_resource(CodPl, '/codpl/<int:cod_pl>', endpoint='codpl')
    api.__created__ = True
    return api


class CodPl(Resource):
    def get(self, cod_pl):
        if not Money.objects(cod_pl=cod_pl)[:1]:
            data = load_data_to_mongo(cod_pl)
        periods_and_suppliers = dict()
        periods_and_suppliers['periods'] = get_periods()
        periods_and_suppliers['suppliers'] = get_suppliers()
        return periods_and_suppliers
