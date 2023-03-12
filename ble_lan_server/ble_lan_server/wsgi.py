import os
from ble_lan_server.app import create_app
import logging

app = create_app(os.environ.get('APP_ENV') if os.environ.get('APP_ENV') else 'Local')
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
