from infrastructure.database.mongo import db


class Location(db.Document):
    # Location Data
    user_id = db.StringField()
    lat = db.FloatField()
    long = db.FloatField()
    accuracy = db.FloatField()
    speed = db.FloatField()
    timestamp = db.DateTimeField()
