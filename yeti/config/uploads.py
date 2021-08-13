import os
import errno

UPLOAD_DIR = os.getcwd() + "/uploads"

try:
    os.makedirs(UPLOAD_DIR)
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise


def get_available_uploads():
    available_uploads = []

    for root, dirs, files in os.walk(UPLOAD_DIR):
        for name in dirs:
            if os.listdir(os.path.join(root, name)):
                available_uploads.append(name)

    return available_uploads
