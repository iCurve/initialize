# coding=utf-8
import uuid

from .base_test_case import IcurveTestCase

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class BandTestCase(IcurveTestCase):

    def test_get_band(self):
        # prepare
        data_name = str(uuid.uuid4()).replace('-', '')
        test_case = '20170828000000,52794.0,0\r\n' \
                    '20170828000100,52558.0,0\r\n' \
                    '20170828000200,51845.0,0\r\n' \
                    '20170828000300,51096.0,0\r\n' \
                    '20170828000400,51300.0,0\r\n' \
                    '20170828000500,50922.0,0\r\n' \
                    '20170828000600,50516.0,0\r\n' \
                    '20170828000700,50289.0,0\r\n' \
                    '20170828000800,49476.0,0\r\n' \
                    '20170828001000,49284.0,0\r\n' \
                    '20170828001100,49476.0,1\r\n'
        message = 'GET /v1/data/<dataName>/band/<bandName> 正常情况'
        self.client.post(path='/v1/data/%s' % data_name, data={'file': (StringIO(test_case), 'test.csv')})
        # test
        response = self.client.get(path='/v1/data/%s/band/%s' % (data_name, 'test'))
        self.assertJsonResponse(response, 200, message)

    def test_delete_band(self):
        # prepare
        data_name = str(uuid.uuid4()).replace('-', '')
        test_case = '20170828000000,52794.0,0\r\n' \
                    '20170828000100,52558.0,0\r\n' \
                    '20170828000200,51845.0,0\r\n' \
                    '20170828000300,51096.0,0\r\n' \
                    '20170828000400,51300.0,0\r\n' \
                    '20170828000500,50922.0,0\r\n' \
                    '20170828000600,50516.0,0\r\n' \
                    '20170828000700,50289.0,0\r\n' \
                    '20170828000800,49476.0,0\r\n' \
                    '20170828001000,49284.0,0\r\n' \
                    '20170828001100,49476.0,1\r\n'
        message = 'DELETE /v1/data/<dataName>/band/<bandName> 正常情况'
        self.client.post(path='/v1/data/%s' % data_name, data={'file': (StringIO(test_case), 'test.csv')})
        # test
        response = self.client.delete(path='/v1/data/%s/band/%s' % (data_name, 'test'))
        self.assertJsonResponse(response, 200, message)