import json

from infrastructure.database.redis import redis_cache
from domain.services.locations import location_save_service


class RedisEventHandler:

    cache = redis_cache
    pubsub = cache.redis.pubsub()

    def __init__(self):
        self.pubsub.psubscribe(**{"__keyevent@0__:expired": self.event_handler})
        self.thread = self.pubsub.run_in_thread(sleep_time=0.01)
        self.location_save_service = location_save_service

    def event_handler(self, msg):
        print("Handler", msg)
        try:
            key = msg["data"]
            if "s_key" in key:
                key = key.replace("s_key:", "")
                value = json.loads(self.cache.get(key))
                self.location_save_service.execute(value)
                self.cache.remove(key)
                print(f"Got Value {value} for key {key}")
        except Exception as e:
            print(str(e))


redis_event_handler = RedisEventHandler()
