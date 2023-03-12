import datetime

from flask_restx import Resource, Namespace, fields
from flask import jsonify, make_response, request
from api.operations.client import Client
from ble_lan_server.api.db.models.agent import Agent, Localization
from ble_lan_server.api.decorators import token_required, admin_required

ns = Namespace("agent", description="Agent's endpoint")

localization_model = ns.model('Localization', {
    'timestamp': fields.String(required=True, description='The timestamp', default=datetime.datetime.now()),
    'latitude': fields.Float(required=True, description='The agent geolocalization'),
    'longitude': fields.Float(required=True, description='The agent geolocalization'),
})

agent_model = ns.model('Agent',{
    'id': fields.String(required=True, description='The Agent unique identifier'),
    'active': fields.Boolean(required=False, description='The Agent state'),
    'localization': fields.List(fields.Nested(localization_model)),
})


@ns.route('/<string:agent_id>')
@ns.response(404, 'Agent not found')
@ns.param('id', 'The Agent identifier')
class AgentEndpoint(Resource):
    '''Show a single client item'''
    @ns.doc('get_agent')
    @ns.marshal_with(agent_model)
    @admin_required
    def get(self, agent_id):
        """ Muestra un agente concreto """
        agent = Agent.objects.get_or_404(id=agent_id)
        return make_response(jsonify(agent), 200)

    @ns.doc('delete_agent')
    @ns.response(204, 'Agent deleted')
    def delete(self, agent_id):
        """Delete an agent given its identifier"""
        data_object_access = Client()
        data_object_access.delete(agent_id)
        return '', 204

    @ns.expect(agent_model)
    @ns.marshal_with(agent_model)
    def put(self, agent_id):
        """Update a client given its identifier"""
        data_object_access = Client()
        return data_object_access.update(agent_id, ns.payload)


@ns.route('/')
class AgentEndpoint(Resource):
    """Show a single client item"""
    @ns.doc('list_clients')
    @ns.marshal_with(agent_model)
    #@admin_required
    def get(self):
        """List all clients"""
        result = None
        try:
            agents = Agent.objects()
            result = {"agent": agents}
        except Exception as ex:
            ns.logger.error(repr(ex))

        return make_response(jsonify(result), 200)

    @ns.expect(agent_model)
    @ns.marshal_with(agent_model)
    def post(self):
        """Update a client given its identifier"""
        result = None
        try:
            body = request.get_json()
            agent = Agent(**body).save()
        except Exception as ex:
            ns.logger.error(repr(ex))
        return make_response(jsonify(agent))