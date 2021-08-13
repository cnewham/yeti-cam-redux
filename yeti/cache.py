from datetime import datetime, timedelta
import json


class Cache(object):
    cached = None

    def __init__(self, cache_file):
        self.cache_file = cache_file

    def save(self, cached, expire_in_mins):
        cached["expire"] = (datetime.now() + timedelta(minutes=expire_in_mins)).isoformat()
        self.cached = cached

        with open(self.cache_file, 'w') as output:
            json.dump(self.cached, output)

    def get(self):
        if self.cached:
            return self.cached

        try:
            with open(self.cache_file, 'r') as input:
                self.cached = json.load(input)
        except Exception:
            self.cached = {}

        return self.cached

    def expired(self):
        return not self.cached or datetime.strptime(self.cached["expire"], "%Y-%m-%dT%H:%M:%S.%f") <= datetime.now()


class WeatherCache(Cache):
    def __init__(self):
        super(WeatherCache, self).__init__("weather.json")
