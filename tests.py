from tornado.testing import AsyncHTTPTestCase
import rest_api
import json


class TestRestApi(AsyncHTTPTestCase):
    # tests for the method adding up numbers
    def get_app(self):
        return rest_api.make_app()
