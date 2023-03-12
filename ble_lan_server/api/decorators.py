from flask import request


def admin_required(func):
    def inner(*args):
        cert = request.headers.get('X-SSL-CERT')
        apikey = request.headers.get('X-API-KEY')
        print("Check if admin")
        func(*args)
    return inner

def token_required(func):
    def inner(*args):
        cert = request.headers.get('X-SSL-CERT')
        apikey = request.headers.get('X-API-KEY')
        print("Check if token is valid")
        func(*args)
    return inner