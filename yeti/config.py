import os
import errno
import pickledb

import logging
logger = logging.getLogger(__name__)

CONFIG_DIR = os.getcwd() + "/config"

try:
    os.makedirs(CONFIG_DIR)
except OSError as ex:
    if ex.errno != errno.EEXIST:
        raise
    
WEATHER_LOCATION = "weather_location"
WEATHER_WU_KEY = "wu_key"
WEATHER_AMBIENT_APP_KEY = "ambient_app_key"
WEATHER_AMBIENT_API_KEY = "ambient_api_key"
WEATHER_STATION = "station"
WEATHER_FEATURES = "features"
WEATHER_EXPIRE_MIN = "expire_min"
WEATHER_DARKSKY_API_KEY = "darksky_api_key"


def weather():
    db = pickledb.load(CONFIG_DIR + "/" + "weather.db", True)
    
    if not db.get(WEATHER_LOCATION):
        db.set(WEATHER_LOCATION, "NA")

    if not db.get(WEATHER_WU_KEY):
        db.set(WEATHER_WU_KEY, "NA")

    if not db.get(WEATHER_AMBIENT_APP_KEY):
        db.set(WEATHER_AMBIENT_APP_KEY, "NA")

    if not db.get(WEATHER_AMBIENT_API_KEY):
        db.set(WEATHER_AMBIENT_API_KEY, "NA")

    if not db.get(WEATHER_STATION):
        db.set(WEATHER_STATION, "KPACLEAR5")

    if not db.get(WEATHER_EXPIRE_MIN):
        db.set(WEATHER_EXPIRE_MIN, 10)

    if not db.get(WEATHER_DARKSKY_API_KEY):
        db.set(WEATHER_DARKSKY_API_KEY, "NA")

    return db

