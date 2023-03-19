from flask import jsonify, make_response, request
from flask_restx import Resource, Namespace, fields
from werkzeug.exceptions import NotFound
from mongoengine.queryset.visitor import Q
from ble_lan_server.api.db.models.ble_device import BleDevice, Detections  # , Localization
from ble_lan_server.api.decorators import token_required, admin_required

ns = Namespace("ble", description="BLE's endpoint")

localization_model = ns.model('Localization', {
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
})

detection_model = ns.model('DetectionModel',
                           {'timestamp': fields.Float(required=True, description='The timestamp in unix time'),
                            'rssi': fields.Float(required=True,
                                                 description='The agent distance to the agent localization'),
                            'detected_by_agent': fields.String(required=True,
                                                               description='The agent which detect the BLE device'),
                            'agent_localization': fields.Nested(localization_model)
                            })

ble_device_model = ns.model('BLEDevice', {
    'mac': fields.String(required=True, description='MAC adress of the BLE device'),
    'certified': fields.Boolean(required=False, description='Tell us if the device is known or not'),
    'detections': fields.List(fields.Nested(detection_model))
})


@ns.route('/<string:mac>')
@ns.response(404, 'BLE not found')
@ns.param('id', 'The BLE identifier')
class BLEEndpoint(Resource):
    '''Works with a single BLE item'''

    @ns.doc('get_ble')
    # @ns.marshal_with(ble_device_model)
    @token_required
    def get(self, mac):
        '''Fetch a given BLE'''
        result = None
        try:
            ble_device = BleDevice.objects().get_or_404(mac=mac)
            result = {"agent": ble_device}

        except Exception as ex:
            ns.logger.error(repr(ex))
            result = make_response('Error {}'.format(repr(ex)), 400)

        return make_response(jsonify(result), 200)

    @ns.doc('delete_ble')
    @ns.response(204, 'BLE deleted')
    @admin_required
    def delete(self, mac):
        '''Delete a BLE given its identifier'''
        result = None
        try:
            ble_device = BleDevice.objects.get_or_404(mac=mac)
            if ble_device:
                ble_device.delete()
                result = make_response('BLEDevice deleted', 204)
            else:
                result = make_response('BLEDevice not found', 204)
        except Exception as ex:
            result = make_response('Error {}'.format(repr(ex)), 400)

        return result


@ns.route('/')
class BLEsEndpoint(Resource):
    '''Operations over multiple BLEs'''

    @ns.doc('list_ble')
    # @ns.marshal_with(ble_device_model)
    # @token_required
    def get(self):
        '''List all BLEs'''
        result = None
        try:
            ble_device = BleDevice.objects()
            result = {"agent": ble_device}

        except Exception as ex:
            ns.logger.error(repr(ex))
            result = make_response('Error {}'.format(repr(ex)), 400)

        return make_response(jsonify(result), 200)

    @ns.doc('post_or_update_bles')
    @ns.expect(ble_device_model)
    # @ns.marshal_with(ble_device_model)
    # @token_required
    def put(self):
        '''Post or update a BLE Device'''
        ble_device = None
        try:
            body = request.get_json()
            # Primero vemos si el Dispositivo existe, en cuyo caso lo actualizamos
            ble_device = BleDevice.objects.get_or_404(mac=body['mac'])

            # if ble_device:
            detection = body['detections'][0]
            new_detection = Detections(**detection)
            ble_device.detections.append(new_detection)
            ble_device.save()
        except NotFound:
            try:
                ble_device = BleDevice(**body)
                ble_device.save()
            except Exception as ex:
                raise ex
        except Exception as ex:
            ns.logger.error(repr(ex))

        return make_response(jsonify(ble_device), 200)


@ns.route('/all_detections_by_agent/<string:detected_by_agent>')
@ns.response(404, 'BLE not found')
class BLEEndpoint3(Resource):
    '''Works with Agents to obtain BLEs item'''

    @ns.doc('get_all_ble_by_agent')
    # @token_required
    def get(self, detected_by_agent):
        '''Fetch a given BLE'''
        result = None
        try:
            ble_devices = BleDevice.objects(detections__detected_by_agent=detected_by_agent).all()
            result = {"agent_devices": ble_devices}

        except Exception as ex:
            ns.logger.error(repr(ex))
            result = make_response('Error {}'.format(repr(ex)), 400)

        return make_response(jsonify(result), 200)


@ns.route('/last_detection_by_agent/<string:detected_by_agent>')
@ns.response(404, 'BLE not found')
class BLEEndpoint4(Resource):
    '''Works with Agents to obtain BLEs item'''

    @ns.doc('get_all_ble_by_agent')
    # @token_required
    def get(self, detected_by_agent):
        '''Fetch a given BLE'''
        result = None
        try:
            # Utilizamos la función filter de MongoEngine para buscar los documentos que contienen
            # el valor deseado en la propiedad "detected_by_agent"
            # y los ordenamos por el valor del campo "timestamp" en orden descendente
            # Obtener el valor máximo de timestamp de todas las listas de detections de todos los documentos BleDevice

            max_timestamp = BleDevice.objects.aggregate(*[
                {
                    '$match': {
                        'detections.detected_by_agent': detected_by_agent
                    }
                },
                {
                    '$unwind': '$detections'
                },
                {
                    '$match': {
                        'detections.detected_by_agent': detected_by_agent
                    }
                },
                {
                    '$group': {
                        '_id': None,
                        'max_timestamp': {'$max': '$detections.timestamp'}
                    }
                }
            ]).next().get('max_timestamp')

            ble_devices = BleDevice.objects(
                Q(detections__detected_by_agent=detected_by_agent) &
                Q(detections__timestamp=max_timestamp)
            ).order_by('detections.timestamp').all()

            new_ble_devices = []
            for ble_device in ble_devices:
                ble_device.detections = [detection for detection in ble_device.detections if
                                         detection.timestamp == max_timestamp]
                new_ble_devices.append(ble_device)

            result = {'ble_devices': new_ble_devices}

        except Exception as ex:
            ns.logger.error(repr(ex))
            result = make_response('Error {}'.format(repr(ex)), 400)

        return make_response(jsonify(result), 200)
