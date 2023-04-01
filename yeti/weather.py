from datetime import datetime, timedelta
import json
import requests
from yeti import astro
from yeti.config import WeatherConfig
from yeti.cache import WeatherCache
import logging

logger = logging.getLogger(__name__)

config = WeatherConfig()
cache = WeatherCache()
cached = cache.get()


def build_weatherbit_url():
    lat, lon = config.get(config.LOCATION).split(',')

    return f"http://api.weatherbit.io/v2.0/forecast/daily" \
           f"?lat={lat}&lon={lon}" \
           f"&key={config.get(config.WEATHERBIT_API_KEY)}" \
           f"&units=I"


def build_ambient_weather_url():
    return f"https://api.ambientweather.net/v1/devices" \
           f"?applicationKey={config.get(config.AMBIENT_APP_KEY)}" \
           f"&apiKey={config.get(config.AMBIENT_API_KEY)}"


def refresh():
    try:
        logger.info("Retrieving weather data from Ambient Weather")
        with requests.get(build_ambient_weather_url()) as response:
            response.raise_for_status()

            result = json.loads(response.text)
            current = result[0]["lastData"]

        logger.info("Retrieving weather data from WeatherBit")
        with requests.get(build_weatherbit_url()) as response:
            response.raise_for_status()
            forecast = json.loads(response.text)

        if "alerts" in forecast:  # TODO: this doesn't exist in this WeatherBit API call
            cached["alerts"] = []

            for item in forecast["alerts"]:
                alert = {
                    "title": item["title"],
                    "severity": item["severity"],
                    "time": datetime.fromtimestamp(item["time"]).isoformat(),
                    "expires": datetime.fromtimestamp(item["expires"]).isoformat(),
                    "uri": item["uri"]
                }

                cached["alerts"].append(alert)

        cached["longitude"] = forecast["lon"]
        cached["latitude"] = forecast["lat"]

        current_date = datetime.fromtimestamp(current["dateutc"] / 1000)

        cached["current"] = {
            "date": current_date.isoformat(),
            "temp": current["tempf"],
            "apparentTemp": current["feelsLike"],
            "humidity": current["humidity"],
            "indoor": {
                "temp": current["tempinf"],
                "humidity": current["humidityin"]
            },
            "wind": {
                "speed": current["windspeedmph"],
                "direction": current["winddir"],
                "gust": current["windgustmph"]
            },
            "precipitation": {
                "hourly": current["hourlyrainin"],
                "daily": current["dailyrainin"],
                "weekly": current["weeklyrainin"]
            },
            "astrology": astro.tojson(forecast["lat"], forecast["lon"])
        }

        cached["forecast"] = []
        for day in forecast["data"]:
            data = {
                "summary": day["weather"]["description"],
                "date": datetime.fromtimestamp(day["ts"]).isoformat(),
                "icon": day["weather"]["icon"],
                "humidity": day["rh"] / 100,
                "dewPoint": day["dewpt"],
                "cloudCover": day["clouds"] / 100,
                "visibility": day["vis"],
                "pressure": day["pres"],
                "ozone": day["uv"],
                "temp": {
                    "high": day["high_temp"],
                    "low": day["low_temp"],
                    "apparentHigh": day["app_max_temp"],
                    "apparentLow": day["app_min_temp"],
                },
                "wind": {
                    "speed": day["wind_spd"],
                    "direction": day["wind_dir"],
                    "gust": day["wind_gust_spd"]
                }
            }

            if day["snow"] > 0:
                precip_type = "snow"
            elif day["precip"] > 0:
                precip_type = "rain"
            else:
                precip_type = ""

            precip_acc = day["snow"] if day["snow"] > 0 else day["precip"]

            data["precipitation"] = {
                "rain": day["precip"],
                "snow": day["snow"],
                "type": precip_type,
                "accumulation": precip_acc,
                "probability": day["pop"] / 100
            }

            data["astrology"] = astro.tojson(forecast["lat"], forecast["lon"],
                                             datetime.fromtimestamp(day["ts"]))

            cached["forecast"].append(data)
            cached["current"]["icon"] = cached["forecast"][0]["icon"]

        cache.save(cached, config.get(config.EXPIRE_MIN))
    except:
        logger.exception("An error occurred while attempting to gather weather data")
        raise


def get(force=False):
    logger.info("Getting weather data")

    # Refresh data if it's the first time, it's expired or the force flag is set
    if cache.expired() or force:
        refresh()

    return cached


if __name__ == "__main__":
    refresh()

    exit()
