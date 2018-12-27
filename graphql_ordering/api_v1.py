import json
from logging import getLogger
from pprint import pprint
from flask_restful import Api, Resource
from .models import Money
from .database import load_data_to_mongo, get_periods, get_suppliers
from .schema import schema

__all__ = ["create_api"]
__doc__ = "Information about api"

logger = getLogger('api')


def create_api(api=None):
    api = api if isinstance(api, Api) else Api(prefix='/v1')
    if getattr(api, '__created__', None):
        return api

    api.add_resource(CodPl, '/codpl/<int:cod_pl>', endpoint='codpl')
    api.add_resource(ByOwner, '/byowner/<int:i_owner>', endpoint='byowner')
    api.add_resource(ByPeriod, '/byperiod/<int:period_>', endpoint='byperiod')
    api.add_resource(GetForMakePdf,
                     '/getpdf/<int:cod_pl>/<int:i_owner>/<int:s_period>/<int:e_period>',
                     endpoint='getpdf')

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


class ByOwner(Resource):
    def get(self, i_owner):
        if i_owner:
            periods = dict()
            periods['periods'] = get_periods(i_owner)
            return periods


class ByPeriod(Resource):
    def get(self, i_owner):
        if i_owner:
            periods = dict()
            periods['periods'] = get_periods(i_owner)
            return periods


class GetForMakePdf(Resource):
    def get(self, i_owner, s_period, e_period, cod_pl):
        if not Money.objects(cod_pl=cod_pl)[:1]:
            data = load_data_to_mongo(cod_pl)
        # data = Money.objects(cod_pl=cod_pl)
        # data = data.objects(i_owner=i_owner)
        # data = data.objects(for_period__lt=e_period)
        # data = data.objects(for_period__gt=s_period)
        data = Money.objects(cod_pl=cod_pl,
                             i_owner=i_owner,
                             for_period__lt=e_period,
                             for_period__gt=s_period
                             ).to_json()

        pprint(set(Money.objects.distinct("typerec")))

        return data
