import os
import sys

from flask import Flask
from flask_restful import Api


def initialize_app(app):
    # initialize and configure the app

    app.config["PROPAGATE_EXCEPTIONS"] = False
    app.config["MONGODB_SETTINGS"] = {
        "host": os.environ["MONGODB_HOST"],
        "username": os.environ["MONGODB_USERNAME"],
        "password": os.environ["MONGODB_PASSWORD"],
        "db": "webapp",
    }

    with app.app_context():
        from application.routes import initialize_routes
        from domain.services.redis_event_handler import redis_event_handler
        from infrastructure.database.mongo import initialize_mongo_db
        from infrastructure.database.redis import redis_cache

        # Initialize plugins
        api = Api(app)

        # Initialize db
        initialize_mongo_db(app)

        # Initialize routes
        initialize_routes(api)


def event_handler(self, msg):
    print("Handler", msg)


app = Flask(__name__)
initialize_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
