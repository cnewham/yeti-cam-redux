from flask_restful import Api
from yeti import app
from yeti.api.resources import HelloWorld

BASE_ENDPOINT = "/api/v1"
api = Api(app)

api.add_resource(HelloWorld, BASE_ENDPOINT + '/')
