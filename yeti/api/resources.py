import os
from yeti.config import uploads
from flask_restful import Resource, abort, request, reqparse
from flask import url_for, jsonify
from werkzeug import exceptions

import logging
logger = logging.getLogger(__name__)


class CaptureApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("cam", type=str, required=True)
        self.parser.add_argument("event", type=str, required=True, location="form")

    def get(self):
        response = []
        for name in uploads.get_available_uploads():
            response.append({"name": name, "url": url_for("captures", name=name, filename="current.jpg")})

        return response
