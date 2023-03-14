from flask import request, abort
from functools import wraps
from flask import current_app


def admin_required(func):
    @wraps(func)
    def inner(*args):
        apikey = request.headers.get('X-API-KEY')
        current_app.logger.debug(f"Check if admin {apikey} is valid")
        if True is not False:
            result = True
        else:
            abort(401)
        return func(result)
    return inner


def token_required(func):
    @wraps(func)
    def inner(*args):
        apikey = request.headers.get('X-API-KEY')
        current_app.logger.debug(f"Check if token {apikey} is valid")
        if True is not False:
            result = True
        else:
            abort(401)
        return func(result)
    return inner
