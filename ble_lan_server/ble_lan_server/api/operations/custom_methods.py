from flask import jsonify, current_app, Response, abort
from flask import make_response as flask_make_response


def make_response(data, code):
    try:
        return flask_make_response(jsonify(data), code)
    except TypeError as e:
        current_app.logger.error(repr(e))
        return flask_make_response(data, code)
