import os
import random
import string
import secrets


class BaseEnvironment(object):
    SECRET_KEY = ''.join(random.choices(string.ascii_lowercase, k=50)) if "SECRET_KEY" not in os.environ.keys() else \
        os.environ['SECRET_KEY']
    SERVICE_PORT = 80 if "PORT" not in os.environ.keys() else os.environ['PORT']
    HOST = '0.0.0.0'
    DEBUG = True
    API_KEY_LENGTH = 16
    ADMIN_API_KEY = secrets.token_urlsafe(API_KEY_LENGTH) \
        if "ADMIN_API_KEY" not in os.environ.keys() else \
        os.environ['ADMIN_API_KEY']
    DEFAULT_PERIOD = 10  # Period time in seconds of detected BLE's of an agent


class LocalEnvironment(BaseEnvironment):
    FRONTEND_DOMAIN = "http://127.0.0.1:4200"
    SERVICE_PORT = 5000 if "PORT" not in os.environ.keys() else os.environ['PORT']

    MONGODB_SETTINGS = {
        'db': 'tfm-ble',
        'host': '127.0.0.1',
        'port': 27017,
        'username': 'admin',
        'password': 'admin',
    }
    APP_DOMAIN = "http://localhost:4200"
    # MONGODB_HOST = "mongodb://tfm-ble:tfm-ble@localhost:27017/?authMechanism=DEFAULT&authSource=tfm-ble"


class AzurePrimaryEnvironment(BaseEnvironment):
    MONGODB_SETTINGS = {
        'db': os.environ["AZURE_DB_NAME"] if "AZURE_DB_NAME" in os.environ else "",
        'host': os.environ["AZURE_DB_HOST"] if "AZURE_DB_HOST" in os.environ else "",
        'port': int(os.environ["AZURE_DB_PORT"]) if "AZURE_DB_PORT" in os.environ else 27017,
        'username': os.environ["AZURE_DB_PRIMARY_USER"] if "AZURE_DB_PRIMARY_USER" in os.environ else "",
        'password': os.environ["AZURE_DB_PRIMARY_PASS"] if "AZURE_DB_PRIMARY_PASS" in os.environ else "",
        'ssl': True,
        'retrywrites': False
    }
    MONGODB_CONNECTION = f"mongodb://{MONGODB_SETTINGS['username']}:{MONGODB_SETTINGS['password']}" \
                         f"@{MONGODB_SETTINGS['host']}:{MONGODB_SETTINGS['port']}/" \
                         f"?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=" \
                         f"@{MONGODB_SETTINGS['username']}@"

    FRONTEND_DOMAIN = os.environ["FRONTEND_DOMAIN"] if "FRONTEND_DOMAIN" in os.environ \
        else "https://tfmble.azurewebsites.net"


class AzureSecondaryEnvironment(BaseEnvironment):
    MONGODB_SETTINGS = {
        'db': os.environ["AZURE_DB_NAME"] if "AZURE_DB_NAME" in os.environ else "",
        'host': os.environ["AZURE_DB_HOST"] if "AZURE_DB_HOST" in os.environ else "",
        'port': int(os.environ["AZURE_DB_PORT"]) if "AZURE_DB_PORT" in os.environ else 27017,
        'username': os.environ["AZURE_DB_SECONDARY_USER"] if "AZURE_DB_SECONDARY_USER" in os.environ else "",
        'password': os.environ["AZURE_DB_SECONDARY_PASS"] if "AZURE_DB_SECONDARY_PASS" in os.environ else "",
        'ssl': True,
        'retrywrites': False
    }
    MONGODB_CONNECTION = f"mongodb://{MONGODB_SETTINGS['username']}:{MONGODB_SETTINGS['password']}" \
                         f"@{MONGODB_SETTINGS['host']}:{MONGODB_SETTINGS['port']}/" \
                         f"?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=" \
                         f"@{MONGODB_SETTINGS['username']}@"
    FRONTEND_DOMAIN = "https://tfmble.azurewebsites.net"


class AzureTestEnvironment(BaseEnvironment):
    MONGODB_SETTINGS = {
        'db': os.environ["AZURE_DB_NAME"] if "AZURE_DB_NAME" in os.environ else "test",
        'host': os.environ["AZURE_DB_HOST"] if "AZURE_DB_HOST" in os.environ else "",
        'port': int(os.environ["AZURE_DB_PORT"]) if "AZURE_DB_PORT" in os.environ else 27017,
        'username': os.environ["AZURE_DB_PRIMARY_USER"] if "AZURE_DB_PRIMARY_USER" in os.environ else "",
        'password': os.environ["AZURE_DB_PRIMARY_PASS"] if "AZURE_DB_PRIMARY_PASS" in os.environ else "",
        'ssl': True,
        'retrywrites': False
    }
    MONGODB_CONNECTION = f"mongodb://{MONGODB_SETTINGS['username']}:{MONGODB_SETTINGS['password']}" \
                         f"@{MONGODB_SETTINGS['host']}:{MONGODB_SETTINGS['port']}/" \
                         f"?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=" \
                         f"@{MONGODB_SETTINGS['username']}@"
    FRONTEND_DOMAIN = os.environ["FRONTEND_DOMAIN"] if "FRONTEND_DOMAIN" in os.environ \
        else "https://tfmble.azurewebsites.net"
