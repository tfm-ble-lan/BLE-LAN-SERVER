from flask import send_from_directory, render_template, Blueprint

import os

views = Blueprint('views', __name__, template_folder='templates', static_folder='static')


@views.route('/')
def welcome():
    return render_template('home.html')


@views.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join("ble_lan_server/static", "favicon.ico"),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
