import mongoengine as me
from flask_mongoengine import MongoEngine

db = MongoEngine()


class Localization(db.EmbeddedDocument):
    latitude = me.FloatField(required=True)
    longitude = me.FloatField(required=True)

    def parse_to_view(self):
        pretty_view = {
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
        return pretty_view


class Detections(db.EmbeddedDocument):
    timestamp = me.FloatField(required=True)
    rssi = me.FloatField(required=True)
    detected_by_agent = me.StringField(required=True)
    agent_localization = me.EmbeddedDocumentField(Localization)

    def parse_to_view(self):
        pretty_view = {
            "timestamp": self.timestamp,
            "rssi": self.rssi,
            "detected_by_agent": self.detected_by_agent,
            "agent_localization": self.agent_location.parse_to_view(),
        }
        return pretty_view


class BleDevice(db.Document):
    mac = me.StringField(required=True, unique=True)
    certified = me.BooleanField(required=False, default=False)
    detections = me.ListField(me.EmbeddedDocumentField(Detections))

    def parse_to_view(self):
        pretty_view = {
            "mac": self.mac,
            "certified": self.certified,
            "detections": [t.parse_to_view() for t in self.detections],
        }
        return pretty_view
