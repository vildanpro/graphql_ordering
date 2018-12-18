#!/usr/bin/env python
from pprint import pprint
from os import path as op
from flask_script import Manager
from flask_script.commands import ShowUrls
from flask import make_response, jsonify

import graphql_ordering
from graphql_ordering import create_app
modules = [graphql_ordering]

app = create_app()

manager = Manager(app)
manager_show = Manager(usage="Display information about application")

#################
# Base Commands #
#################
manager.add_command("show", manager_show)


@manager.command
def runserver():
    """ Runserver with socketio support """
    return app.run(
        host=app.config.get('START_HOST', '127.0.0.1'),
        port=app.config.get('START_PORT', 5000),
        use_debugger=app.config.get('DEBUG', False),
        use_reloader=True
    )

#################
# Show Commands #
#################


manager_show.add_command('routes', ShowUrls())


def table_print(*headers):
    out = "    ".join(headers)
    print(out)
    print("-" * len(out))


@manager_show.command
def config():
    """ print application config """
    table_print("App Config:")
    pprint(dict(app.config))


@manager_show.command
def structure():
    """ print application structure """
    table_print("Extensions:")
    pprint(app.extensions)

    table_print("Blueprints:")
    pprint(app.blueprints)

    table_print("App:")
    pprint(app)


@manager_show.command
def description(full=False):
    """ print base information """
    for mod in modules:
        table_print(mod.__name__)
        print("Version: {}\nDescription:\n{}\n".format(mod.__version__, mod.__doc__))
        if full and op.exists("README.md"):
            print("Full Description:\n")
            print(open("README.md", 'r').read())


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'Error': 'Not found'}), 404)


if __name__ == "__main__":
    manager.run()
