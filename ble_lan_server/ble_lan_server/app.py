import os
import logging
import sys

from flask import Flask, make_response
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap, WebCDN
#CORS
from flask_cors import CORS
from views import views
from ble_lan_server import blueprint as api_blueprint
from ble_lan_server.api.config import environment


db = MongoEngine()


def create_app():
    flask_app = Flask(__name__)
    with flask_app.app_context():
        # Iniciar aplicación flask más configuración
        cors = CORS(flask_app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
        flask_app.config.from_object(environment)
        flask_app.config.update(ENV=environment)
        flask_app.url_map.strict_slashes = False

        # Iniciar swagger para apidoc y la base de datos
        db.init_app(flask_app)

        Bootstrap(flask_app)
        flask_app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
            'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/')
        flask_app.secret_key = flask_app.config['SECRET_KEY']
        flask_app.config['SESSION_TYPE'] = 'filesystem'
        flask_app.register_blueprint(views, url_prefix="/")
        flask_app.register_blueprint(api_blueprint)

    # Iniciar logger para generar logs en debug a lo largo del código
    logger = logging.getLogger(__name__)
    logger.debug(f'Working in {environment} environment')

    @flask_app.route("/")
    def site_map():
        return make_response("It's working! Please go to /api", 200)
        # links is now a list of url, endpoint tuple

    return flask_app


if __name__ == '__main__':

    app = create_app()
    if os.path.isfile('private_certificate_for_ssl.pem'):
        app.run(debug=True, host='0.0.0.0', ssl_context=(
            'private_certificate_for_ssl.pem', 'private_certificate_for_ssl.key'), port=app.config['SERVICE_PORT'])
    else:
        app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['SERVICE_PORT'])
