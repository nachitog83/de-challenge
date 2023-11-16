import os

from flask import jsonify, make_response, request
from flask_restful import Resource

from domain.dtos.locations import LocationDTO
from domain.exceptions.exceptions import (
    AlreadyCreatedError,
    CoordinatesError,
    TimeStampError,
)
from domain.services.locations import location_cache_service


class Location(Resource):
    def put(self):
        try:
            dto = LocationDTO(**request.json)
        except (CoordinatesError, TimeStampError) as e:
            return make_response(jsonify(message=str(e)), 400)
        except TypeError as e:
            msg = str(e)
            msg = msg.replace("LocationDTO.__init__()", "Request payload")
            return make_response(jsonify(message=msg), 400)

        try:
            location_cache_service.execute(dto)
            return make_response(jsonify(message="success"), 200)
        except AlreadyCreatedError as e:
            return make_response(jsonify(message=str(e)), 200)
        except Exception as e:
            return make_response(jsonify(message=str(e)), 500)


class Root(Resource):
    def get(self):
        return make_response(jsonify(message="Hello World!"), 200)
