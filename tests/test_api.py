import os
import unittest

import mongomock
from truth.truth import AssertThat

from api import main


class TestLocationApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = main.app.test_client()

    @mongomock.patch(servers=((os.environ["MONGODB_HOST"], 27017),))
    def test_should_return_200_when_data_is_valid(self):
        location = {
            "timestamp": "2017-01-01 13:05:12",
            "lat": 40.701,
            "long": -73.916,
            "accuracy": 11.3000021,
            "speed": 1.3999992,
            "user_id": "a1",
        }

        response = self.client.put("/location", json=location)

        AssertThat(response.status_code).IsEqualTo(200)

    @mongomock.patch(servers=((os.environ["MONGODB_HOST"], 27017),))
    def test_should_return_400_when_missing_timestamp(self):
        location = {"lat": 40.701, "long": -73.916, "accuracy": 11.3000021, "speed": 1.3999992, "user_id": "a1"}

        response = self.client.put("/location", json=location)

        AssertThat(response.status_code).IsEqualTo(400)

    @mongomock.patch(servers=((os.environ["MONGODB_HOST"], 27017),))
    def test_should_return_400_when_bad_coordinates(self):
        location = {
            "lat": "not coords",
            "long": "not coords",
            "accuracy": 11.3000021,
            "speed": 1.3999992,
            "user_id": "a1",
        }

        response = self.client.put("/location", json=location)

        AssertThat(response.status_code).IsEqualTo(400)

    @mongomock.patch(servers=((os.environ["MONGODB_HOST"], 27017),))
    def test_should_return_200_when_already_created(self):
        location = {
            "timestamp": "2017-01-01 13:05:12",
            "lat": 40.701,
            "long": -73.916,
            "accuracy": 11.3000021,
            "speed": 1.3999992,
            "user_id": "b1",
        }

        response = self.client.put("/location", json=location)

        AssertThat(response.status_code).IsEqualTo(200)
        AssertThat(response.json["message"]).IsEqualTo("success")
