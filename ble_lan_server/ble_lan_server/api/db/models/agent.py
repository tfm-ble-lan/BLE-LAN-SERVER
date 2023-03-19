import mongoengine as me
from flask_mongoengine import MongoEngine

db = MongoEngine()


class Agent(db.Document):
    name = me.StringField(required=True, unique=True)
    active = me.BooleanField(required=False, default=True)
    bt_address = me.StringField(required=False, default=None)
    api_key = me.StringField(required=False, default=None, unique=True)

    def parse_to_view(self):
        pretty_view = {
            "name": self.name,
            "is_active": self.active,
            "bt_address": self.bt_address,
            "api_key": self.api_key,
        }
        return pretty_view
