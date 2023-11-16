from flask_mongoengine import MongoEngine

db = MongoEngine()

def initialize_mongo_db(app):
    db.init_app(app)