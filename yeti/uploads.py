import os
import shutil
import errno

import logging
logger = logging.getLogger(__name__)

UPLOAD_DIR = os.getcwd() + "/uploads"

try:
    os.makedirs(UPLOAD_DIR)
except OSError as ex:
    if ex.errno != errno.EEXIST:
        raise


def get_available_uploads():
    available_uploads = []

    for root, dirs, files in os.walk(UPLOAD_DIR):
        for name in dirs:
            if os.listdir(os.path.join(root, name)):
                available_uploads.append(name)

    return available_uploads


def process(name, upload, args):
    uploaddir = UPLOAD_DIR + "/" + name
    event = args["event"]

    try:
        os.makedirs(uploaddir)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise

    filename = "%s-%s" % (event, os.path.basename(upload.filename))
    logger.info("Processing %s event for image %s" % (event, filename))
    capture = os.path.join(uploaddir, filename)
    upload.save(capture)
    shutil.copy(capture, os.path.join(uploaddir, "current.jpg"))

    # TODO: Add gdrive support
    os.remove(capture)

    return filename

