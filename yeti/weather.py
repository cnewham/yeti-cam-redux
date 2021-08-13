from datetime import datetime, timedelta
import json
import requests
from yeti import astro, config
from yeti.cache import WeatherCache
import logging
logger = logging.getLogger(__name__)

config_values = config.weather()
cache = WeatherCache()
cached = cache.get()


def build_darksky_url():
    return "https://api.darksky.net/forecast/%s/%s?exclude=minutely,hourly,currently" % (
        config_values.get(config.WEATHER_DARKSKY_API_KEY), config_values.get(config.WEATHER_LOCATION))


def build_ambient_weather_url():
    return "https://api.ambientweather.net/v1/devices?applicationKey=%s&apiKey=%s" % (
        config_values.get(config.WEATHER_AMBIENT_APP_KEY), config_values.get(config.WEATHER_AMBIENT_API_KEY))


def refresh():
    try:
        logger.info("Retrieving weather data from Ambient Weather")
        with requests.get(build_ambient_weather_url()) as response:
            response.raise_for_status()

            result = json.loads(response.text)
            ambient = result[0]["lastData"]

        logger.info("Retrieving weather data from DarkSky")
        with requests.get(build_darksky_url()) as response:
            response.raise_for_status()
            darksky = json.loads(response.text)

        if "alerts" in darksky:
            cached["alerts"] = []

            for item in darksky["alerts"]:
                alert = {
                    "title": item["title"],
                    "severity": item["severity"],
                    "time": datetime.fromtimestamp(item["time"]).isoformat(),
                    "expires": datetime.fromtimestamp(item["expires"]).isoformat(),
                    "uri": item["uri"]
                }

                cached["alerts"].append(alert)

        cached["longitude"] = darksky["longitude"]
        cached["latitude"] = darksky["latitude"]

        current_date = datetime.fromtimestamp(ambient["dateutc"]/1000)

        cached["current"] = {
            "date": current_date.isoformat(),
            "temp": ambient["tempf"],
            "apparentTemp": ambient["feelsLike"],
            "humidity": ambient["humidity"],
            "indoor": {
                "temp": ambient["tempinf"],
                "humidity": ambient["humidityin"]
            },
            "wind": {
                "speed": ambient["windspeedmph"],
                "direction": ambient["winddir"],
                "gust": ambient["windgustmph"]
            },
            "precipitation": {
                "hourly": ambient["hourlyrainin"],
                "daily": ambient["dailyrainin"],
                "weekly": ambient["weeklyrainin"]
            },
            "astrology": astro.tojson(darksky["latitude"], darksky["longitude"])
        }

        cached["forecast"] = []
        for day in darksky["daily"]["data"]:
            forecast = {
                "summary": day["summary"],
                "date": datetime.fromtimestamp(day["time"]).isoformat(),
                "icon": day["icon"],
                "humidity": day["humidity"],
                "dewPoint": day["dewPoint"],
                "cloudCover": day["cloudCover"],
                "visibility": day["visibility"],
                "pressure": day["pressure"],
                "ozone": day["ozone"],
                "temp": {
                    "high": day["temperatureHigh"],
                    "low": day["temperatureLow"],
                    "apparentHigh": day["apparentTemperatureHigh"],
                    "apparentLow": day["apparentTemperatureLow"],
                },
                "wind": {
                    "speed": day["windSpeed"],
                    "direction": day["windBearing"],
                    "gust": day["windGust"],
                    "gustTime": datetime.fromtimestamp(day["windGustTime"]).isoformat()
                },
                "precipitation": {
                    "type": day["precipType"] if "precipType" in day else "",
                    "accumulation": day["precipAccumulation"] if "precipAccumulation" in day else 0,
                    "probability": day["precipProbability"],
                    "intensity": day["precipIntensity"]
                },
                "astrology": astro.tojson(darksky["latitude"], darksky["longitude"],
                                          datetime.fromtimestamp(day["time"]))
            }

            cached["forecast"].append(forecast)
            cached["current"]["icon"] = cached["forecast"][0]["icon"]

        cache.save(cached, config_values.get(config.WEATHER_EXPIRE_MIN))
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
