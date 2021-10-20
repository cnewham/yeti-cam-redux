import os
import errno
import pickledb
import json
import logging
logger = logging.getLogger(__name__)

CONFIG_DIR = os.getcwd() + "/config"

try:
    os.makedirs(CONFIG_DIR)
except OSError as ex:
    if ex.errno != errno.EEXIST:
        raise


class Config(object):
    db = None
    config_file = None

    def __init__(self, config_file):
        self.config_file = config_file
        self.load()

    def load(self):
        self.db = pickledb.load(self.config_file, True)

    def default(self, key, value):
        if not self.db.exists(key):
            self.db.set(key, value)

    def exists(self, key):
        return self.db.exists(key)

    def get(self, key):
        if self.db.exists(key):
            return self.db.get(key)

        raise KeyError("Key (%s) doesn't exist" % key)

    def set(self, key, value):
        self.db.set(key, value)

    def update(self, configs):
        logger.info("Updating configs")

        if not configs or configs is None:
            raise ValueError("No config values have been supplied")

        for key in configs:
            if self.exists(key):
                self.db.set(key, configs[key])

    def to_json(self):
        with open(self.config_file, 'r+') as configdb:
            configs = configdb.read()

        return json.loads(configs)


class WeatherConfig(Config):
    LOCATION = "weather_location"
    WU_KEY = "wu_key"
    AMBIENT_APP_KEY = "ambient_app_key"
    AMBIENT_API_KEY = "ambient_api_key"
    STATION = "station"
    FEATURES = "features"
    EXPIRE_MIN = "expire_min"
    DARKSKY_API_KEY = "darksky_api_key"

    def __init__(self):
        super(WeatherConfig, self).__init__(CONFIG_DIR + "/" + "weather.db")

        self.default(self.LOCATION, "NA")
        self.default(self.WU_KEY, "NA")
        self.default(self.AMBIENT_APP_KEY, "NA")
        self.default(self.AMBIENT_API_KEY, "NA")
        self.default(self.STATION, "KPACLEAR5")
        self.default(self.EXPIRE_MIN, 10)
        self.default(self.DARKSKY_API_KEY, "NA")


class ClientConfig(Config):
    CAPTURE_UPLOAD_MIN = "capture_upload_min"
    MOTION_DETECT_ENABLED = "motion_enabled"
    MOTION_DETECT_START = "motion_start"
    MOTION_DETECT_END = "motion_end"
    MOTION_NIGHT_ONLY = "motion_night_only"
    UPLOAD_THRESHOLD = "upload_threshold"
    CAPTURE_RETENTION_DAYS = "capture_retention_days"

    def __init__(self):
        super(ClientConfig, self).__init__(CONFIG_DIR + "/" + "client.db")
        self.default(self.CAPTURE_UPLOAD_MIN, 60)
        self.default(self.MOTION_DETECT_ENABLED, False)
        self.default(self.MOTION_DETECT_START, None)
        self.default(self.MOTION_DETECT_END, None)
        self.default(self.MOTION_NIGHT_ONLY, False)
        self.default(self.UPLOAD_THRESHOLD, 2)
        self.default(self.CAPTURE_RETENTION_DAYS, 30)


class DriveConfig(Config):
    def __init__(self):
        super(DriveConfig, self).__init__(CONFIG_DIR + "/" + "drive.db")

    def get_folder_id(self, name):
        return self.get(name)


class CamsConfig(Config):
    def __init__(self):
        super(CamsConfig, self).__init__(CONFIG_DIR + "/" + "cams.db")

    def default(self, key, value=None):
        if not self.db.exists(key):
            self.db.dcreate(key)
            self.db.dadd(key, ("hidden", False))
            self.db.dadd(key, ("order", 0))

    def get(self, key):
        if self.db.exists(key):
            return self.db.dgetall(key)

        raise KeyError("Key (%s) doesn't exist" % key)

    def update(self, configs):
        if not configs or configs is None:
            raise ValueError("No values have been supplied")

        for cam in configs.keys():
            for key, value in configs[cam].items():
                self.db.dadd(cam, (key, value))
