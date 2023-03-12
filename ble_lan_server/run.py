from flask import Flask
from server_settings import SECRET_KEY, SERVICE_PORT
from flask_bootstrap import Bootstrap, WebCDN
from views import views
from ble_lan_server import blueprint
import os


app = Flask(__name__)


if __name__ == '__main__':
    Bootstrap(app)
    app.extensions['bootstrap']['cdns']['jquery'] = WebCDN('https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/')
    app.secret_key = SECRET_KEY
    app.config['SESSION_TYPE'] = 'filesystem'
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(blueprint)

    if os.path.isfile('certs/ca.cert.pem'):
        app.run(debug=True, host='0.0.0.0', ssl_context=(
            'certs/ca.cert.pem', 'certs/ca.key'), port=443)
    else:
        app.run(debug=True, host='0.0.0.0', port=SERVICE_PORT)
