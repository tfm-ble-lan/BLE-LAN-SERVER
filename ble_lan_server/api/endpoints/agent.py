import secrets
from flask_restx import Resource, Namespace, fields
from flask import jsonify, request, current_app
from ble_lan_server.api.operations.custom_methods import make_response
from ble_lan_server.api.db.models.agent import Agent
from ble_lan_server.api.decorators import admin_required

ns = Namespace("agent", description="Agent's endpoint")

agent_model = ns.model('Agent',
                       {
                           'name': fields.String(required=True, description='The Agent unique identifier'),
                           'active': fields.Boolean(required=False, description='The Agent state'),
                           'bt_address': fields.String(required=False, description='The Bluetooth MAC Address'),
                       }
                       )


@ns.route('/<string:agent_name>')
@ns.response(404, 'Agent not found')
class AgentEndpoint(Resource):
    '''Show a single client item'''

    @ns.doc('get_agent')
    @admin_required
    # @ns.marshal_with(agent_model)
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
    @admin_required
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
    @admin_required
    # @ns.marshal_with(agent_model)
    def put(self, name):
        """Update a client given its identifier"""
        result = None
        try:
            body = request.get_json()
            agent = Agent.objects.get_or_404(name=name)
            agent.update(**body)
            result = make_response('Agent {} updated'.format(name), 200)
        except Exception as ex:
            result = make_response('Error {}'.format(repr(ex)), 400)

        return result


@ns.route('/')
class AgentEndpoint2(Resource):

    """Show a single client item"""

    @ns.doc('list_clients')
    @admin_required
    # @ns.marshal_with(agent_model)
    def get(self):
        """List all agents"""
        result = None
        try:
            agents = Agent.objects()
            result = make_response({"agent": agents}, 200)
        except Exception as ex:
            current_app.logger.error(repr(ex))
            result = make_response('Error {}'.format(repr(ex)), 400)
        return result

    @ns.expect(agent_model)
    @admin_required
    # @ns.marshal_with(agent_model)
    def put(self):
        """Create an agent if do not exists on the data base"""
        try:
            body = request.get_json()
            if not body:
                raise Exception("Wrong input data")

            body["bt_address"] = body["bt_address"].lower()
            db_agent = Agent.objects(bt_address=body["bt_address"])
            if not db_agent:
                # Agent is not registered
                api_key = secrets.token_urlsafe(current_app.config["API_KEY_LENGTH"])
                body["api_key"] = api_key
                agent = Agent(**body).save()
                result = make_response(agent, 200)
            else:
                # Agent is registered
                db_agent.update(**body)
                result = make_response('Agent state for {} updated'.format(body["name"]), 200)
        except Exception as ex:
            agent = repr(ex)
            current_app.logger.error(agent)
            result = make_response('Error {}'.format(repr(ex)), 400)
        return result
