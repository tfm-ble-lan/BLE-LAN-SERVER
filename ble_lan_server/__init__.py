from flask import Blueprint
from flask_restx import Api
from ble_lan_server.api.endpoints.client import ns as ns1

blueprint = Blueprint("api", __name__, url_prefix="/api")

api = Api(blueprint, version='0.1', title='TFM BLE-LAN API',
    description='API to operate with BLE-LAN server',
)
api.add_namespace(ns1)
