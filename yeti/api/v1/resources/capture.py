from yeti import app, uploads
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
        for name in uploads.get_available_uploads():
            response.append({"name": name, "url": url_for("captures", name=name, filename="current.jpg")})

        return response

    def post(self, name):
        logger.debug("Uploading capture for: " + name)

        args = self.parser.parse_args(request)
        uploaded = request.files['uploads']

        if uploaded and self.allowed_file(uploaded.filename):
            filename = uploads.process(name, uploaded, args)
            return {'filename': filename}, HTTPStatus.CREATED
        else:
            abort(HTTPStatus.BAD_REQUEST)

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].upper() in app.config['ALLOWED_EXTENSIONS']
