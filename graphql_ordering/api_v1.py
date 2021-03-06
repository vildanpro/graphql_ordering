from logging import getLogger
from flask_restful import Api, Resource
from .db import DataLoader

__all__ = ["create_api"]
__doc__ = "Information about api"

logger = getLogger('api')


def create_api(api=None):
    api = api if isinstance(api, Api) else Api(prefix='/v1')
    if getattr(api, '__created__', None):
        return api

    api.add_resource(Test, '/test/<int:cod_pl>/', endpoint='test')

    api.__created__ = True
    return api


class Test(Resource):
    def get(self, cod_pl):
        if DataLoader().load_data_from_sql(cod_pl):
            return True
        else:
            return {
                "Error": "Type of COD_PL must be INT"
            }

