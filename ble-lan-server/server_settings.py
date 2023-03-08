import os
import random
import string

SECRET_KEY = ''.join(random.choices(string.ascii_lowercase, k=50)) if "SECRET_KEY" not in os.environ.keys() else os.environ['SECRET_KEY']
SERVICE_PORT = 5000 if "PORT" not in os.environ.keys() else os.environ['PORT']
