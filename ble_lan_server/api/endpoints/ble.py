from flask_restx import Resource, Namespace, fields
from ble_lan_server.api.operations.client import Client
from flask import request
from ble_lan_server.api.decorators import token_required, admin_required

ns = Namespace("ble", description="BLE's endpoint")

ble_model = ns.model('BLE', {
    'id': fields.String(readonly=True, description='The BLE unique identifier'),
    'ble': fields.String(required=True, description='The BLE details')
})

@ns.route('/<string:id>')
@ns.response(404, 'BLE not found')
@ns.param('id', 'The BLE identifier')
class BLEEndpoint(Resource):
    '''Show a single BLE item'''
    @ns.doc('get_ble')
    @ns.marshal_with(ble_model)
    @token_required
    def get(self, id):
        '''Fetch a given BLE'''
        DAO = Client()
        c = DAO.get(id)
        if not c:
          ns.abort(404, "BLE {} doesn't exist".format(id))
        return c

    @ns.doc('delete_ble')
    @ns.response(204, 'BLE deleted')
    @admin_required
    def delete(self, id):
        '''Delete a BLE given its identifier'''
        DAO = Client()
        DAO.delete(id)
        return '', 204

    @ns.expect(ble_model)
    @ns.marshal_with(ble_model)
    @token_required
    def put(self, id):
        DAO = Client()
        '''Update a BLE given its identifier'''
        return DAO.update(id, ns.payload)

@ns.route('/')
class BLEsEndpoint(Resource):
    '''Operations over multiple BLEs'''
    @ns.doc('list_ble')
    @ns.marshal_with(ble_model)
    @token_required
    def get(self):
        '''List all BLEs'''
        DAO = Client()
        c = DAO.list_all()
        return c

    @ns.doc('update_bles')
    @ns.marshal_with(ble_model)
    def put(self):
        '''Update multiple BLEs'''

        DAO = Client()
        c = DAO.list_all()
        return c
