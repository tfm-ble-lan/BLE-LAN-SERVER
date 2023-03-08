from flask import Flask
from server_settings import SECRET_KEY, SERVICE_PORT
from flask_bootstrap import Bootstrap, WebCDN
from views import views
import os


app = Flask(__name__)


if __name__ == '__main__':
    Bootstrap(app)
    app.extensions['bootstrap']['cdns']['jquery'] = WebCDN('https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/')
    app.secret_key = SECRET_KEY
    app.config['SESSION_TYPE'] = 'filesystem'
    app.register_blueprint(views, url_prefix="/")
    if os.path.isfile('private_certificate_for_ssl.pem'):
        app.run(debug=True, host='0.0.0.0', ssl_context=(
            'private_certificate_for_ssl.pem', 'private_certificate_for_ssl.key'), port=SERVICE_PORT)
    else:
        app.run(debug=True, host='0.0.0.0', port=SERVICE_PORT)
