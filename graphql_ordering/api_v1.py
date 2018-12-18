from logging import getLogger
from flask_restful import Api, Resource
from .database import init_db


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
        return init_db(cod_pl)
