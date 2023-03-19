from flask import request  # , abort
from functools import wraps
from flask import current_app
from ble_lan_server.api.db.models.agent import Agent


def admin_required(func):
    @wraps(func)
    def inner(*args, **kwarg):

        apikey = request.headers.get('X-API-KEY')
        c = current_app.config
        if apikey == current_app.config["ADMIN_API_KEY"]:
            current_app.logger.debug(f"Admin Token {apikey} is valid")
        else:
            current_app.logger.debug(f"Admin Token {apikey} is not valid but I let you anyway")
            # abort(401)
        return func(*args,  **kwarg)
    return inner


def token_required(func):
    @wraps(func)
    def inner(*args, **kwarg):
        apikey = request.headers.get('X-API-KEY')
        agent = Agent.objects(api_key=apikey)
        if agent:
            current_app.logger.debug(f"Token {apikey} is valid, agent: {agent.first().name}")
        else:
            current_app.logger.debug(f"Token {apikey} is not valid but I let you anyway")
            # abort(401)
        return func(*args,  **kwarg)
    return inner
