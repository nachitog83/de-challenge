import os

from redis import StrictRedis


class RedisCache:
    def __init__(self):
        self.redis = StrictRedis(
            host=os.environ["REDIS_HOST"],
            port=os.environ["REDIS_PORT"],
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=10,
        )
        self.redis.config_set("notify-keyspace-events", "Ex")
        self._ttl = 60

    def set(self, key, value):
        """
        :param key: The key for the lookup
        :param value: The value for the lookup
        :param expiration: Expiration in seconds
        """

        s_key = f"s_key:{key}"
        ttl = self.redis.ttl(s_key)
        ttl = ttl if ttl > 0 else self._ttl
        s_result = self.redis.set(s_key, "", ex=ttl)
        result = self.redis.set(key, value, ex=ttl + 5)
        return result

    def get(self, key):
        """
        :param name: The key for lookup
        :return: value associated with the key, or None if the key is missing or expired
        """
        return self.redis.get(key)

    def remove(self, key):
        return self.redis.delete(key)

    def expire(self, key, expiration):
        self.redis.expire(key, expiration)


redis_cache = RedisCache()
