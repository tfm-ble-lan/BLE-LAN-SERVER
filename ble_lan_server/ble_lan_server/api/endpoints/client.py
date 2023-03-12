from flask_restx import Resource, Namespace, fields
from ble_lan_server.api.decorators import token_required, admin_required
from api.operations.client import Client


ns = Namespace("client", description="Client's endpoint")

client_model = ns.model('Client', {
    'id': fields.String(readonly=True, description='The client unique identifier'),
    'client': fields.String(required=True, description='The client details')
})

@ns.route('/<string:id>')
@ns.response(404, 'Client not found')
@ns.param('id', 'The Client identifier')
class ClientEndpoint(Resource):
    '''Show a single client item'''
    @ns.doc('get_client')
    @ns.marshal_with(client_model)
    @admin_required
    def get(self, id):
        '''Fetch a given client'''
        data_object_access = Client()
        c = data_object_access.get(id)
        if not c:
          ns.abort(404, "Client {} doesn't exist".format(id))
        return c

    @ns.doc('delete_client')
    @ns.response(204, 'Client deleted')
    @admin_required
    def delete(self, id):
        '''Delete a client given its identifier'''
        data_object_access = Client()
        data_object_access.delete(id)
        return '', 204

    @ns.expect(client_model)
    @ns.marshal_with(client_model)
    @admin_required
    def put(self, id):
        data_object_access = Client()
        '''Update a client given its identifier'''
        return data_object_access.update(id, ns.payload)

@ns.route('/')
class ClientsEndpoint(Resource):
    '''Show a single client item'''
    @ns.doc('list_clients')
    @ns.marshal_with(client_model)
    @admin_required
    def get(self):
        '''List all clients'''
        data_object_access = Client()
        c = data_object_access.list_all()
        return c
