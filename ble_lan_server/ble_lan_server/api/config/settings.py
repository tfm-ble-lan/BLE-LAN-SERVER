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
        'db': os.environ["AZURE_DB_NAME"],
        'host': os.environ["AZURE_DB_HOST"],
        'port': int(os.environ["AZURE_DB_PORT"]),
        'username': os.environ["AZURE_DB_PRIMARY_USER"],
        'password': os.environ["AZURE_DB_PRIMARY_PASS"],
        'ssl': True
    }
    MONGODB_CONNECTION = f"mongodb://{os.environ['AZURE_DB_PRIMARY_USER']}:{os.environ['AZURE_DB_PRIMARY_PASS']}" \
                         f"@tfm-ble.mongo.cosmos.azure.com:10255/" \
                         f"?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@tfm-ble@"


class AzureSecondaryEnvironment(BaseEnvironment):
    MONGODB_SETTINGS = {
        'db': os.environ["AZURE_DB_NAME"],
        'host': os.environ["AZURE_DB_HOST"],
        'port': int(os.environ["AZURE_DB_PORT"]),
        'username': os.environ["AZURE_DB_SECONDARY_USER"],
        'password': os.environ["AZURE_DB_SECONDARY_PASS"],
        'ssl': True
    }
    MONGODB_HOST = f"mongodb://{os.environ['AZURE_DB_SECONDARY_USER']}:{os.environ['AZURE_DB_SECONDARY_PASS']}@" \
                   f"tfm-ble.mongo.cosmos.azure.com:10255/" \
                   f"?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@tfm-ble@"
