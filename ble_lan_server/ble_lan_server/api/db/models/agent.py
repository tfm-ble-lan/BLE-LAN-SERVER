import mongoengine as me


class Localization(me.EmbeddedDocument):
    timestamp = me.StringField(required=True)
    latitude = me.FloatField(required=True)
    longitude = me.FloatField(required=True)


    def parse_to_view(self):
        pretty_view = {
            "timestamp": self.timestamp,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
        return pretty_view


class Agent(me.Document):
    id = me.StringField(required=True, primary_key=True)
    localization = me.ListField(me.EmbeddedDocumentField(Localization))
    active = me.BooleanField(required=False, default=True)

    def parse_to_view(self):
        pretty_view = {
            "id": self.id,
            "localization_historical": [t.parse_to_view() for t in self.localization],
            "is_active": self.active,
        }
        return pretty_view
