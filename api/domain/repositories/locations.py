from domain.models.location import Location
from domain.repositories import BaseRepository

"""
City repository inherited from BaseRepository.
We could define specific behaviour for city domain logic here

"""


class LocationsRepository(BaseRepository):
    pass


locations_repo = LocationsRepository(Location)
