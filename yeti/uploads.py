import os
import shutil
import errno
import gzip
from flask import abort
from http import HTTPStatus

from yeti import cams
from yeti.config import DriveConfig
import yeti.drive as drive

import logging
logger = logging.getLogger(__name__)

UPLOAD_DIR = os.getcwd() + "/uploads"

try:
    os.makedirs(UPLOAD_DIR)
except OSError as ex:
    if ex.errno != errno.EEXIST:
        raise

config = DriveConfig()


def get_available_uploads():
    available_uploads = []

    for root, dirs, files in os.walk(UPLOAD_DIR):
        for name in dirs:
            if os.listdir(os.path.join(root, name)):
                available_uploads.append(name)
                cams.default(name)

    return available_uploads


def process(name, upload, args):
    uploaddir = UPLOAD_DIR + "/" + name
    event = args["event"].strip()

    try:
        os.makedirs(uploaddir)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise

    filename = "%s-%s" % (event, os.path.basename(upload.filename))
    logger.info("Processing %s event for image %s" % (event, filename))
    capture = os.path.join(uploaddir, filename)

    if "gzip" in args and args["gzip"]:
        logger.debug("gzip, decompressing...")
        try:
            with open(capture, "wb") as decompressed:
                decompressed.write(gzip.decompress(upload.read()))
        except gzip.BadGzipFile:
            abort(HTTPStatus.BAD_REQUEST)
    else:
        upload.save(capture)

    shutil.copy(capture, os.path.join(uploaddir, "current.jpg"))

    if config.exists(name):
        drive.upload(capture, event, config.get_folder_id(name))

    os.remove(capture)

    if not cams.exists(name):
        cams.default(name)

    return filename

