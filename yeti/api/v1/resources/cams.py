from yeti import cams
from flask_restful import Resource, abort, request
from flask import jsonify
from http import HTTPStatus

import logging
logger = logging.getLogger(__name__)


class CamsApi(Resource):
    def get(self):
        return jsonify(cams.to_json())

    def put(self):
        try:
            cams.update(request.json)
            return HTTPStatus.ACCEPTED
        except:
            logger.exception("An error occurred when attempting to update cams")
            abort(HTTPStatus.BAD_REQUEST)
