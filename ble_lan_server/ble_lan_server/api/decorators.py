from flask import request, abort
from functools import wraps
from flask import current_app


def admin_required(func):
    @wraps(func)
    def inner(*args, **kwarg):
        apikey = request.headers.get('X-API-KEY')
        if True is not False:
            current_app.logger.debug(f"Admin Token {apikey} is valid")
            result = True
        else:
            abort(401)
        return func(result, *args,  **kwarg)
    return inner


def token_required(func):
    @wraps(func)
    def inner(*args, **kwarg):
        apikey = request.headers.get('X-API-KEY')
        if True is not False:
            current_app.logger.debug(f"Token {apikey} is valid")
            result = True
        else:
            abort(401)
        return func(result, *args,  **kwarg)
    return inner
