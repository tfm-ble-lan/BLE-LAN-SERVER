import os
import sys
import ble_lan_server.api.config.settings

# Creamos el objeto de settings conveniente para el entorno que recibimos desde APP_ENV
APP_ENV = os.environ.get('APP_ENV') if os.environ.get('APP_ENV') else os.environ.get('APP_ENV', 'Local')
environment = getattr(sys.modules['ble_lan_server.api.config.settings'], '{0}Environment'.format(APP_ENV))()
