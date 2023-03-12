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
    #MONGODB_HOST = "mongodb://tfm-ble:tfm-ble@localhost:27017/?authMechanism=DEFAULT&authSource=tfm-ble"


class AzurePrimaryEnvironment(BaseEnvironment):
    MONGODB_SETTINGS = {
        'db': 'tfm-ble',
        'host': 'tfm-ble.mongo.cosmos.azure.com',
        'port': 10255,
        'username': 'tfm-ble',
        'password': 'pbl6bMPRRrYWLlmRlP6aH9sCCX8MmWHoXiyJ6svC36wSHylBrXSxTtmN7z5LfdlwU5nmCXByH8ImACDb4Vff4g==',
    }
    MONGODB_HOST = "mongodb://tfm-ble:pbl6bMPRRrYWLlmRlP6aH9sCCX8MmWHoXiyJ6svC36wSHylBrXSxTtmN7z5LfdlwU5nmCXByH8ImACDb4Vff4g==@tfm-ble.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@tfm-ble@"


class AzureSecondaryEnvironment(BaseEnvironment):
    MONGODB_SETTINGS = {
        'db': 'tfm-ble',
        'host': 'tfm-ble.mongo.cosmos.azure.com',
        'port': 10255,
        'username': 'tfm-ble',
        'password': 'OJH1JPPiui1ly61UXCCamHUYTap6YB5CTz9kU9OctZwEGrm9tcaGkEHjulqVmVqx1M1hTXDS0PzeACDbOsQFHw==',
    }
    MONGODB_HOST = "mongodb://tfm-ble:OJH1JPPiui1ly61UXCCamHUYTap6YB5CTz9kU9OctZwEGrm9tcaGkEHjulqVmVqx1M1hTXDS0PzeACDbOsQFHw==@tfm-ble.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@tfm-ble@"
