from flask import jsonify, current_app, Response
from flask import make_response as flask_make_response

def make_response(data, code):
    try:
        return flask_make_response(jsonify(data), code)
    except TypeError as e:
        current_app.logger.error(repr(e))
        if isinstance(data, Response):
            return Response
        return flask_make_response(jsonify(data), code)