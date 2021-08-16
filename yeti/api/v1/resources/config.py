from yeti.config import ClientConfig
from flask_restful import Resource, abort, request
from flask import jsonify
from http import HTTPStatus

import logging
logger = logging.getLogger(__name__)

config = ClientConfig()


class ConfigApi(Resource):
    def get(self):
        return jsonify(config.to_json())

    def put(self):
        try:
            config.update(request.json)
            return HTTPStatus.ACCEPTED
        except:
            logger.exception("An error occurred when attempting to update cams")
            abort(HTTPStatus.BAD_REQUEST)
