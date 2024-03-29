import os
import logging
import errno
from logging.handlers import RotatingFileHandler
from yeti.config import CamsConfig
from flask import Flask

# INITIALIZE LOGGING

if "LOG_DIR" in os.environ:
    LOG_DIR = os.environ["LOG_DIR"]
else:
    LOG_DIR = os.getcwd()

LOG_LEVEL = logging.DEBUG
LOG_FILENAME = "%s/yeticam.log" % LOG_DIR

logging.basicConfig(level=LOG_LEVEL,
                    format="%(name)-12s: %(levelname)-8s %(message)s")

handler = RotatingFileHandler(
              LOG_FILENAME, maxBytes=500000, backupCount=5)

formatter = logging.Formatter("%(asctime)-15s %(levelname)-8s %(name)-20s %(message)s")
handler.setFormatter(formatter)

logging.getLogger('').addHandler(handler)
logging.getLogger('botocore').setLevel(logging.WARN)

# INITIALIZE SERVER

app = Flask(__name__, static_folder='www/static', template_folder='www/templates')
app.config['ALLOWED_EXTENSIONS'] = ['JPG', 'JPEG', 'TAR.GZ']

# INITIALIZE CAMS

UPLOAD_DIR = os.getcwd() + "/uploads"

try:
    os.makedirs(UPLOAD_DIR)
except OSError as ex:
    if ex.errno != errno.EEXIST:
        raise

cams = CamsConfig()

for name in os.listdir(UPLOAD_DIR):
    cams.default(name)

