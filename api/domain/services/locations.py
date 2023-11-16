import json
from dataclasses import asdict

import numpy as np
from mongoengine import Document

from infrastructure.database.redis import redis_cache
from domain.dtos.locations import LocationDTO
from domain.exceptions.exceptions import AlreadyCreatedError
from domain.repositories.locations import LocationsRepository, locations_repo


class LocationDataCacheService:
    def __init__(self):
        self.locations_repo: LocationsRepository = locations_repo
        self.cache = redis_cache

    def execute(self, dto: LocationDTO) -> Document:
        timestamp = dto.timestamp.strftime("%Y-%m-%dT%H:%M")

        loc = self.locations_repo.get_by_attr(user_id=dto.user_id, timestamp=timestamp)
        if loc:
            raise AlreadyCreatedError(f"Record already created for user {dto.user_id} and timestamp {timestamp}")

        key = "_".join([dto.user_id, timestamp])
        data = asdict(dto)
        data["timestamp"] = timestamp
        stored = self.cache.get(key)
        if stored:
            stored = json.loads(stored)
            data["lat"] = np.average([data["lat"], stored["lat"]])
            data["long"] = np.average([data["long"], stored["long"]])
            data["accuracy"] = np.average([data["accuracy"], stored["accuracy"]])
            data["speed"] = np.average([data["speed"], stored["speed"]])

        value = json.dumps(data)
        self.cache.set(key, value)


class LocationSaveService:
    def __init__(self):
        self.locations_repo: LocationsRepository = locations_repo

    def execute(self, data: dict) -> Document:
        self.locations_repo.create(**data)


location_cache_service = LocationDataCacheService()
location_save_service = LocationSaveService()
