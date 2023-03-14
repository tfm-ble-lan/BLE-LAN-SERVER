from flask import Blueprint
from flask_restx import Api
from ble_lan_server.api.endpoints.client import ns as ns1
from ble_lan_server.api.endpoints.ble import ns as ns2
from ble_lan_server.api.endpoints.agent import ns as ns3

blueprint = Blueprint("api", __name__, url_prefix="/api")

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(blueprint, version='0.1', title='TFM BLE-LAN API',
          description='API to operate with BLE-LAN server',
          authorizations=authorizations, security='apikey')
api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
