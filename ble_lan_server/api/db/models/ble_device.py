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


class Manufacturer(db.EmbeddedDocument):
    id = me.IntField(required=True)
    name = me.StringField(required=True)

    def parse_to_view(self):
        pretty_view = {
            "id": self.id,
            "name": self.name,
        }
        return pretty_view


class Detections(db.EmbeddedDocument):
    timestamp = me.FloatField(required=True)
    rssi = me.FloatField(required=True)
    tx_power = me.FloatField(required=False)
    detected_by_agent = me.StringField(required=True)
    agent_localization = me.EmbeddedDocumentField(Localization)

    def parse_to_view(self):
        pretty_view = {
            "timestamp": self.timestamp,
            "rssi": self.rssi,
            "tx_power": self.tx_power,
            "detected_by_agent": self.detected_by_agent,
            "agent_localization": self.agent_location.parse_to_view(),
        }
        return pretty_view


class BleDevice(db.Document):
    address = me.StringField(required=True, unique=True)
    name = me.StringField(required=False)
    bluetooth_address = me.IntField(required=False)
    certified = me.BooleanField(required=False, default=False)
    detections = me.ListField(me.EmbeddedDocumentField(Detections))
    manufacturer = me.EmbeddedDocumentField(Manufacturer)

    def parse_to_view(self):
        pretty_view = {
            "address": self.address,
            "certified": self.certified,
            "detections": [t.parse_to_view() for t in self.detections],
        }
        return pretty_view
