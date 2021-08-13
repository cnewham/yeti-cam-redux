from yeti import weather
from flask_restful import Resource
from http import HTTPStatus

import logging
logger = logging.getLogger(__name__)


class WeatherApi(Resource):
    def get(self):
        return weather.get()