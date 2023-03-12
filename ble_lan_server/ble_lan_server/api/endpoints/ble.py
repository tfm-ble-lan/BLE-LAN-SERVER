from flask_restx import Resource, Namespace, fields
from ble_lan_server.api.operations.client import Client
from ble_lan_server.api.decorators import token_required, admin_required

ns = Namespace("ble", description="BLE's endpoint")

detection_model = ns.model('DetectionModel',
                           {'timestamp': fields.DateTime(readonly=True, description='The timestamp'),
                            'rssi': fields.Float(required=True, description='The agent geolocalization'),
                            'detected_by_agent': fields.String(required=True, description='The agent geolocalization')
                            })

ble_device_model = ns.model('BLEDevice', {
    'mac': fields.String(readonly=True, description='The Agent unique identifier'),
    'certified': fields.Boolean(required=False, description='The Agent state'),
    'detections': fields.List(fields.Nested(detection_model))
})


@ns.route('/<string:mac>')
@ns.response(404, 'BLE not found')
@ns.param('id', 'The BLE identifier')
class BLEEndpoint(Resource):
    '''Show a single BLE item'''

    @ns.doc('get_ble')
    @ns.marshal_with(ble_device_model)
    @token_required
    def get(self, mac):
        '''Fetch a given BLE'''
        DAO = Client()
        c = DAO.get(mac)
        if not c:
            ns.abort(404, "BLE {} doesn't exist".format(mac))
        return c

    @ns.doc('delete_ble')
    @ns.response(204, 'BLE deleted')
    @admin_required
    def delete(self, mac):
        '''Delete a BLE given its identifier'''
        DAO = Client()
        DAO.delete(mac)
        return '', 204

    @ns.expect(ble_device_model)
    @ns.marshal_with(ble_device_model)
    @token_required
    def put(self, mac):
        DAO = Client()
        '''Update a BLE given its identifier'''
        return DAO.update(mac, ns.payload)


@ns.route('/')
class BLEsEndpoint(Resource):
    '''Operations over multiple BLEs'''

    @ns.doc('list_ble')
    @ns.marshal_with(ble_device_model)
    #@token_required
    def get(self):
        '''List all BLEs'''
        DAO = Client()
        c = DAO.list_all()
        return c

    @ns.doc('update_bles')
    @ns.marshal_with(ble_device_model)
    def put(self):
        '''Update multiple BLEs'''

        DAO = Client()
        c = DAO.list_all()
        return c
