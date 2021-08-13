import os
from yeti import app
from yeti.config.uploads import UPLOAD_DIR
from flask import render_template, send_from_directory, abort
from http import HTTPStatus

import logging
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    try:
        return render_template('viewer.html')
    except Exception as ex:
        logger.error(ex)
        return HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/captures/<path:name>/<path:filename>')
def captures(name, filename):
    upload = UPLOAD_DIR + "/" + name

    if not os.path.isfile(upload + "/" + filename):
        abort(HTTPStatus.NOT_FOUND)

    return send_from_directory(upload, filename)
