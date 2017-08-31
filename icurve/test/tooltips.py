# coding=utf-8

from .base_test_case import IcurveTestCase


class TooltipsTestCase(IcurveTestCase):

    def test_tooltips(self):
        # prepare
        message = 'GET /v1/tooltips 正常情况'
        # test
        response = self.client.get(path='/v1/tooltips')
        self.assertJsonResponse(response, 200, message)
