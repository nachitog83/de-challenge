from dataclasses import dataclass
from datetime import datetime

import pytz
from dateutil import parser
from domain.exceptions.exceptions import CoordinatesError, TimeStampError
from timezonefinder import TimezoneFinder

timezone_finder = TimezoneFinder(in_memory=True)


@dataclass
class LocationDTO:
    user_id: str
    lat: float
    long: float
    accuracy: float
    speed: float
    timestamp: datetime

    def __post_init__(self):
        self.timestamp = self._convert_to_utc(self.timestamp, self.long, self.lat)

    @staticmethod
    def _convert_to_utc(timestamp: datetime, lng: float, lat: float) -> datetime:
        try:
            local_tz = timezone_finder.timezone_at(lng=lng, lat=lat)
        except (TypeError, ValueError) as e:
            raise CoordinatesError(e)

        tz = pytz.timezone(local_tz)

        try:
            naive = parser.parse(timestamp)
        except ValueError as e:
            raise TimeStampError(e)

        local_dt = tz.localize(naive, is_dst=None)
        return local_dt.astimezone(pytz.utc)
