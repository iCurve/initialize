# coding=utf-8

from .base import IcurveTestCase


class MenuTestCase(IcurveTestCase):

    def test_menus(self):
        # prepare
        message = 'GET /v1/menus 正常情况'
        # test
        response = self.client.get(path='/v1/menus')
        self.assertJsonResponse(response, 200, message)
