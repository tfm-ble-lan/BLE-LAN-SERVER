from flask import send_from_directory, render_template, Blueprint, make_response, current_app
from ble_lan_server.api.decorators import admin_required
import json



import os

views = Blueprint('views', __name__, template_folder='templates', static_folder='static')


@views.route('/')
def welcome():
    return render_template('home.html')


@views.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join("ble_lan_server/static", "favicon.ico"),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@admin_required
@views.route('/config')
def config():
    c = current_app.config
    return make_response(str(current_app.config))