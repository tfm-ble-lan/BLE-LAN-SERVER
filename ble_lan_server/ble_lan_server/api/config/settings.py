import os
import random
import string


class BaseEnvironment(object):
    SECRET_KEY = ''.join(random.choices(string.ascii_lowercase, k=50)) if "SECRET_KEY" not in os.environ.keys() else \
        os.environ['SECRET_KEY']
    SERVICE_PORT = 80 if "PORT" not in os.environ.keys() else os.environ['PORT']
    HOST = '0.0.0.0'
    DEBUG = True


class LocalEnvironment(BaseEnvironment):
    MONGODB_SETTINGS = {
        'db': 'tfm-ble',
        'host': '127.0.0.1',
        'port': 27017,
        'username': 'admin',
        'password': 'admin',
    }
    # MONGODB_HOST = "mongodb://tfm-ble:tfm-ble@localhost:27017/?authMechanism=DEFAULT&authSource=tfm-ble"


class AzurePrimaryEnvironment(BaseEnvironment):
    MONGODB_SETTINGS = {
        'db': os.environ["AZURE_DB_NAME"] if "AZURE_DB_NAME" in os.environ else "",
        'host': os.environ["AZURE_DB_HOST"] if "AZURE_DB_HOST" in os.environ else "",
        'port': int(os.environ["AZURE_DB_PORT"]) if "AZURE_DB_PORT" in os.environ else 27017,
        'username': os.environ["AZURE_DB_PRIMARY_USER"] if "AZURE_DB_PRIMARY_USER" in os.environ else "",
        'password': os.environ["AZURE_DB_PRIMARY_PASS"] if "AZURE_DB_PRIMARY_PASS" in os.environ else "",
        'ssl': True
    }
    MONGODB_CONNECTION = f"mongodb://{MONGODB_SETTINGS['username']}:{MONGODB_SETTINGS['password']}" \
                         f"@{MONGODB_SETTINGS['host']}:{MONGODB_SETTINGS['port']}/" \
                         f"?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=" \
                         f"@{MONGODB_SETTINGS['username']}@"


class AzureSecondaryEnvironment(BaseEnvironment):
    MONGODB_SETTINGS = {
        'db': os.environ["AZURE_DB_NAME"] if "AZURE_DB_NAME" in os.environ else "",
        'host': os.environ["AZURE_DB_HOST"] if "AZURE_DB_HOST" in os.environ else "",
        'port': int(os.environ["AZURE_DB_PORT"]) if "AZURE_DB_PORT" in os.environ else 27017,
        'username': os.environ["AZURE_DB_SECONDARY_USER"] if "AZURE_DB_SECONDARY_USER" in os.environ else "",
        'password': os.environ["AZURE_DB_SECONDARY_PASS"] if "AZURE_DB_SECONDARY_PASS" in os.environ else "",
        'ssl': True
    }
    MONGODB_CONNECTION = f"mongodb://{MONGODB_SETTINGS['username']}:{MONGODB_SETTINGS['password']}" \
                         f"@{MONGODB_SETTINGS['host']}:{MONGODB_SETTINGS['port']}/" \
                         f"?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=" \
                         f"@{MONGODB_SETTINGS['username']}@"


class AzureTestEnvironment(BaseEnvironment):
    MONGODB_SETTINGS = {
        'db': os.environ["AZURE_DB_NAME"] if "AZURE_DB_NAME" in os.environ else "test",
        'host': os.environ["AZURE_DB_HOST"] if "AZURE_DB_HOST" in os.environ else "",
        'port': int(os.environ["AZURE_DB_PORT"]) if "AZURE_DB_PORT" in os.environ else 27017,
        'username': os.environ["AZURE_DB_PRIMARY_USER"] if "AZURE_DB_PRIMARY_USER" in os.environ else "",
        'password': os.environ["AZURE_DB_PRIMARY_PASS"] if "AZURE_DB_PRIMARY_PASS" in os.environ else "",
        'ssl': True
    }
    MONGODB_CONNECTION = f"mongodb://{MONGODB_SETTINGS['username']}:{MONGODB_SETTINGS['password']}" \
                         f"@{MONGODB_SETTINGS['host']}:{MONGODB_SETTINGS['port']}/" \
                         f"?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=" \
                         f"@{MONGODB_SETTINGS['username']}@"
