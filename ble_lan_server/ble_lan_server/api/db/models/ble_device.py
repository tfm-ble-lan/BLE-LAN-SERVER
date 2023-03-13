import mongoengine as me


class Detections(me.EmbeddedDocument):
    timestamp = me.StringField(required=True)
    rssi = me.FloatField(required=True)
    detected_by_agent = me.StringField(required=True)

    def parse_to_view(self):
        pretty_view = {
            "timestamp": self.timestamp,
            "rssi": self.rssi,
            "detected_by_agent": self.detected_by_agent
        }
        return pretty_view


class BleDevice(me.Document):
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
