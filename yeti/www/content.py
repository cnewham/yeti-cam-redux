import os
from yeti import app, drive
from yeti.uploads import UPLOAD_DIR
from flask import request, redirect, url_for, render_template, send_from_directory, abort
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


@app.route('/weather')
def weather():
    return render_template('weather.html')


@app.route('/drive/auth')
def google_drive_auth():
    auth = drive.Authorize(url_for('google_drive_auth', _external=True))
    code = request.args.get('code')
    error = request.args.get('error')

    try:
        if error:
            logger.error("An error occurred while attempting to authorize Google Drive: %s" % error)
            return error
        elif code:
            logger.info("Updating credentials with code %s" % code)
            auth.complete(code)
            return redirect(url_for('index'))
    except Exception as ex:
        return ex.args, 401

    return redirect(auth.start())

