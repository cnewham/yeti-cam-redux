from flask_restful import Api
from yeti import app
from yeti.api.resources import CaptureApi

BASE_ENDPOINT = "/api/v1"
api = Api(app)

api.add_resource(CaptureApi, BASE_ENDPOINT + '/capture')
