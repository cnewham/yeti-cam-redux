from yeti import app, uploads, cams
from flask_restful import Resource, abort, request, reqparse
from flask import url_for
from http import HTTPStatus

import logging
logger = logging.getLogger(__name__)


class CaptureApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("event", type=str, required=True, location="form")

    def get(self):
        response = []
        for name in cams.available():
            capture = {
                "name": name,
                "url": url_for("captures", name=name, filename="current.jpg")
            }

            if cams.exists(name):
                for prop, value in cams.get(name).items():
                    capture[prop] = value

            response.append(capture)

        return response

    def post(self, name):
        logger.debug("Uploading capture (size %s) for: %s" % (request.content_length, name))

        args = self.parser.parse_args(request)

        if 'uploads-gzip' in request.files:
            uploaded = request.files['uploads-gzip']
            args["gzip"] = True
        else:
            uploaded = request.files['uploads']

        if uploaded and self.allowed_file(uploaded.filename):
            filename = uploads.process(name, uploaded, args)
            return {'filename': filename}, HTTPStatus.CREATED
        else:
            abort(HTTPStatus.BAD_REQUEST)

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].upper() in app.config['ALLOWED_EXTENSIONS']
