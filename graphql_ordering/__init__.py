from flask import Flask
from config.json import Config
from logging.config import dictConfig
from .api_v1 import create_api as v1
from mssql import connect as ms
from .mssqldb import MSqlDBLoader
from flask_graphql import GraphQLView
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

	app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

	return app
