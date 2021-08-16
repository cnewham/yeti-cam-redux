from flask_restful import Api
from yeti import app
from yeti.api.v1.resources.capture import CaptureApi
from yeti.api.v1.resources.weather import WeatherApi
from yeti.api.v1.resources.cams import CamsApi

BASE_ENDPOINT = "/api/v1"
api = Api(app)

api.add_resource(CaptureApi, BASE_ENDPOINT + '/capture', BASE_ENDPOINT + '/capture/<string:name>',
                 endpoint='capture-v1')

api.add_resource(WeatherApi, BASE_ENDPOINT + '/weather', endpoint='weather.v1')

api.add_resource(CamsApi, BASE_ENDPOINT + '/cams', endpoint='cams.v1')
