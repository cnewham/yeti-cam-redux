from flask_restful import Api
from yeti import app
from yeti.api.capture import CaptureApi

BASE_ENDPOINT = "/api/v1"
api = Api(app)

api.add_resource(CaptureApi, BASE_ENDPOINT + '/capture', BASE_ENDPOINT + '/capture/<string:name>',
                 endpoint='capture-v1')
