import datetime

from flask_restx import Resource, Namespace, fields
from flask import jsonify, make_response, request
from ble_lan_server.api.db.models.agent import Agent
from ble_lan_server.api.decorators import token_required, admin_required

ns = Namespace("agent", description="Agent's endpoint")

agent_model = ns.model('Agent',
                       {
                           'name': fields.String(required=True, description='The Agent unique identifier'),
                           'active': fields.Boolean(required=False, description='The Agent state'),
                       }
                       )


@ns.route('/<string:agent_name>')
@ns.response(404, 'Agent not found')
class AgentEndpoint(Resource):
    '''Show a single client item'''

    @ns.doc('get_agent')
    # @ns.marshal_with(agent_model)
    #@admin_required
    def get(self, agent_name):
        """ Muestra un agente concreto """
        result = None
        try:
            agent = Agent.objects.get_or_404(name=agent_name)
            result = make_response(jsonify(agent), 200)
        except Exception as ex:
            result = make_response(repr(ex), 400)

        return result

    @ns.doc('delete_agent')
    @ns.response(204, 'Agent deleted')
    def delete(self, agent_name):
        """Delete an agent given its identifier"""
        result = None
        try:
            agent = Agent.objects.get_or_404(name=agent_name)
            if agent:
                agent.delete()
                result = make_response('Agent deleted', 204)
            else:
                result = make_response('Agent not found', 204)
        except Exception as ex:
            result = make_response('Error {}'.format(repr(ex)), 400)

        return result

    @ns.expect(agent_model)
    #@ns.marshal_with(agent_model)
    def put(self, name):
        """Update a client given its identifier"""
        result = None
        try:
            body = request.get_json()
            agent = Agent.objects.get_or_404(name=name)
            agent.update(**body)
            result = make_response('Agent {} updated'.format(name), 204)
        except Exception as ex:
            result = make_response('Error {}'.format(repr(ex)), 400)

        return result


@ns.route('/')
class AgentEndpoint2(Resource):
    """Show a single client item"""

    @ns.doc('list_clients')
    # @ns.marshal_with(agent_model)
    # @admin_required
    def get(self):
        """List all agents"""
        result = None
        try:
            agents = Agent.objects()
            result = {"agent": agents}

        except Exception as ex:
            ns.logger.error(repr(ex))
            result = make_response('Error {}'.format(repr(ex)), 400)

        return make_response(jsonify(result), 200)

    @ns.expect(agent_model)
    # @ns.marshal_with(agent_model)
    def post(self):
        """Update a client given its identifier"""
        result = None
        agent = None
        try:
            body = request.get_json()
            agent = Agent(**body).save()
        except Exception as ex:
            ns.logger.error(repr(ex))
        return make_response(jsonify(agent), 200)
