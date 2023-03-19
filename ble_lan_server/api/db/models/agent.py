import mongoengine as me
from flask_mongoengine import MongoEngine

db = MongoEngine()


class Agent(db.Document):
    name = me.StringField(required=True, unique=True)
    active = me.BooleanField(required=False, default=True)

    def parse_to_view(self):
        pretty_view = {
            "id": self.name,
            "is_active": self.active,
        }
        return pretty_view
