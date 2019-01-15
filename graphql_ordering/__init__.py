from pprint import pprint
from flask import Flask, json, request
from config.json import Config
from logging.config import dictConfig
from .api_v1 import create_api as v1
from mssql import connect as ms
from .mssqldb import MSqlDBLoader
from flask_graphql import GraphQLView
from .database import create_monog_db as mongo
from .schema import schema


__version__ = "1.0"
__doc__ = "Information about application"
__all__ = ["create_app"]


def create_app(app=None, config=None):
    config = config if config is not None else Config()
    dictConfig(config.get('logging')) if config.get('logging') is not None else None
    app = app if isinstance(app, Flask) else Flask(__name__, static_folder=None)
    app.config.from_object(config.extract('app', uppercase=True))
    v1().init_app(app)
    ms(**config.database)
    mongo()
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

    @app.route("/", methods=['POST'])
    def graphlql_query():
        data = json.loads(request.data)
        return json.dumps(schema.execute(data['query']).data)

    return app
